# Author: Roberto Doriguzzi-Corin
# Project: Course on Network Intrusion and Anomaly Detection with Machine Learning
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
"""Replay a PCAP while adding a small random delay to each packet gap."""

from __future__ import annotations

import argparse
import os
import random
import time
from pathlib import Path

from scapy.all import IP, IPv6, PcapReader, PcapWriter, Raw, TCP, UDP, sendp  # type: ignore[import-untyped]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Replay packets from a PCAP on a network interface, adding a random "
            "delay to each inter-arrival time (IAT)."
        )
    )
    parser.add_argument("pcap", type=Path, help="input PCAP file")
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("-i", "--interface", help="egress network interface for replay")
    destination.add_argument("-o",
        "--output-pcap", type=Path,
        help="write a new PCAP with adjusted timestamps instead of replaying",
    )
    parser.add_argument(
        "--min-delay-ms", type=float, default=1.0,
        help="minimum random delay added to each IAT in milliseconds (default: 1)",
    )
    parser.add_argument(
        "--max-delay-ms", type=float, default=10.0,
        help="maximum random delay added to each IAT in milliseconds (default: 10)",
    )
    parser.add_argument(
        "--min-length-change", type=int, default=0, metavar="BYTES",
        help="minimum random packet length change in bytes (default: 0)",
    )
    parser.add_argument(
        "--max-length-change", type=int, default=0, metavar="BYTES",
        help="maximum random packet length change in bytes (default: 0)",
    )
    parser.add_argument(
        "--min-ttl", type=int, default=0, metavar="HOPS",
        help="minimum random TTL (default: 0)",
    )
    parser.add_argument(
        "--max-ttl", type=int, default=0, metavar="HOPS",
        help="maximum random TTL (default: 0 meaning no change)",
    )
    parser.add_argument(
        "--perturb-ip-flags", action="store_true",
        help="randomly change IPv4 DF and MF flags",
    )
    parser.add_argument(
        "--min-tcp-window", type=int, default=0, metavar="BYTES",
        help="minimum random TCP window size (default: 0, disabled)",
    )
    parser.add_argument(
        "--max-tcp-window", type=int, default=0, metavar="BYTES",
        help="maximum random TCP window size (default: 0, disabled)",
    )
    return parser.parse_args()


def perturb_packet_length(packet, min_change: int, max_change: int):
    """Change packet size and recalculate affected IP/transport header fields."""
    change = random.randint(min_change, max_change)
    if change > 0:
        packet.add_payload(Raw(load=os.urandom(change)))
    elif change < 0:
        new_length = len(packet) + change
        if new_length < 1:
            raise ValueError(f"Length change {change} would remove the entire packet")
        packet = packet.__class__(bytes(packet)[:new_length])

    # Scapy recalculates these fields when serializing if they are unset.
    for layer_type in packet.layers():
        layer = packet.getlayer(layer_type)
        if isinstance(layer, IP):
            layer.len = None
            layer.chksum = None
        elif isinstance(layer, IPv6):
            layer.plen = None
        if isinstance(layer, UDP):
            layer.len = None
        if hasattr(layer, "chksum"):
            layer.chksum = None
    return packet


def perturb_ttl(packet, min_ttl: int, max_ttl: int):
    """Apply a random TTL or IPv6 Hop Limit change, if the packet has one."""
    ip_layer = packet.getlayer(IP)
    ipv6_layer = packet.getlayer(IPv6)

    if ip_layer is not None and max_ttl > 0:
        updated_ttl = random.randint(min_ttl, max_ttl)
        ip_layer.ttl = updated_ttl
        ip_layer.chksum = None

    return packet


def perturb_ip_flags(packet):
    """Randomly set IPv4 Don't Fragment and More Fragments flags."""
    ip_layer = packet.getlayer(IP)
    if ip_layer is not None:
        flags = int(ip_layer.flags)
        # Keep the reserved bit unchanged; randomize DF (bit 1) and MF (bit 0).
        flags = (flags & ~0x3) | random.randint(0, 1) | (random.randint(0, 1) << 1)
        ip_layer.flags = flags
        ip_layer.chksum = None
    return packet


def perturb_tcp_window(packet, min_window: int, max_window: int):
    """Set a random TCP advertised window size when the packet has a TCP layer."""
    tcp_layer = packet.getlayer(TCP)
    if tcp_layer is not None and max_window > 0:
        tcp_layer.window = random.randint(min_window, max_window)
        tcp_layer.chksum = None
    return packet


def modified_packets(
    pcap_path: Path,
    min_delay_ms: float,
    max_delay_ms: float,
    min_length_change: int,
    max_length_change: int,
    min_ttl_change: int,
    max_ttl_change: int,
    min_tcp_window: int,
    max_tcp_window: int,
    perturb_flags: bool,
):
    """Yield packets with adjusted timestamps and their adjusted inter-packet delays."""
    previous_timestamp: float | None = None
    modified_timestamp: float | None = None

    with PcapReader(str(pcap_path)) as capture:
        for packet in capture:
            timestamp = float(packet.time)

            delay = 0.0
            if previous_timestamp is None:
                modified_timestamp = timestamp
            else:
                original_gap = max(0.0, timestamp - previous_timestamp)
                added_delay = random.uniform(min_delay_ms, max_delay_ms) / 1000
                delay = original_gap + added_delay
                modified_timestamp += delay

            packet.time = modified_timestamp
            packet = perturb_packet_length(packet, min_length_change, max_length_change)
            packet = perturb_ttl(packet, min_ttl_change, max_ttl_change)
            packet = perturb_tcp_window(packet, min_tcp_window, max_tcp_window)
            if perturb_flags:
                packet = perturb_ip_flags(packet)
            yield packet, delay
            previous_timestamp = timestamp


def replay(
    pcap_path: Path,
    interface: str,
    min_delay_ms: float,
    max_delay_ms: float,
    min_length_change: int,
    max_length_change: int,
    min_ttl: int,
    max_ttl: int,
    min_tcp_window: int,
    max_tcp_window: int,
    perturb_flags: bool,
) -> int:
    """Replay packets with adjusted inter-arrival times, returning the count sent."""
    sent = 0
    for packet, delay in modified_packets(
        pcap_path, min_delay_ms, max_delay_ms, min_length_change, max_length_change,
        min_ttl, max_ttl, min_tcp_window, max_tcp_window, perturb_flags,
    ):
        if sent:
            time.sleep(delay)
        sendp(packet, iface=interface, verbose=False)
        sent += 1
    return sent


def save_modified_pcap(
    pcap_path: Path,
    output_path: Path,
    min_delay_ms: float,
    max_delay_ms: float,
    min_length_change: int,
    max_length_change: int,
    min_ttl: int,
    max_ttl: int,
    min_tcp_window: int,
    max_tcp_window: int,
    perturb_flags: bool,
) -> int:
    """Save packets with adjusted timestamps to a new PCAP and return the count."""
    saved = 0
    with PcapWriter(str(output_path), sync=True) as output:
        for packet, _ in modified_packets(
            pcap_path, min_delay_ms, max_delay_ms, min_length_change, max_length_change,
            min_ttl, max_ttl, min_tcp_window, max_tcp_window, perturb_flags,
        ):
            output.write(packet)
            saved += 1
    return saved


def main() -> int:
    args = parse_args()
    if args.min_delay_ms < 0 or args.max_delay_ms < args.min_delay_ms:
        raise SystemExit("Error: delays must satisfy 0 <= min-delay-ms <= max-delay-ms")
    if args.min_length_change > args.max_length_change:
        raise SystemExit("Error: min-length-change must be <= max-length-change")
    if args.min_ttl > args.max_ttl:
        raise SystemExit("Error: min-ttl must be <= max-ttl")
    if not (0 <= args.min_tcp_window <= args.max_tcp_window <= 65535):
        raise SystemExit("Error: TCP window bounds must satisfy 0 <= min <= max <= 65535")
    if not args.pcap.is_file():
        raise SystemExit(f"Error: PCAP file not found: {args.pcap}")

    if args.output_pcap is not None:
        if args.output_pcap.resolve() == args.pcap.resolve():
            raise SystemExit("Error: output PCAP must differ from input PCAP")
        count = save_modified_pcap(
            args.pcap,
            args.output_pcap,
            args.min_delay_ms,
            args.max_delay_ms,
            args.min_length_change,
            args.max_length_change,
            args.min_ttl,
            args.max_ttl,
            args.min_tcp_window,
            args.max_tcp_window,
            args.perturb_ip_flags,
        )
        print(f"Saved {count} packets to {args.output_pcap}")
    else:
        count = replay(
            args.pcap,
            args.interface,
            args.min_delay_ms,
            args.max_delay_ms,
            args.min_length_change,
            args.max_length_change,
            args.min_ttl,
            args.max_ttl,
            args.min_tcp_window,
            args.max_tcp_window,
            args.perturb_ip_flags,
        )
        print(f"Sent {count} packets on {args.interface}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


