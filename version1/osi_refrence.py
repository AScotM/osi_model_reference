#!/usr/bin/env python3

import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum, auto


class ProtocolType(Enum):
    ROUTING = auto()
    TRANSPORT = auto()
    ENCRYPTION = auto()
    DATA_FORMAT = auto()
    APPLICATION = auto()


@dataclass
class OSILayer:
    number: int
    name: str
    function: str
    protocols: List[str]
    protocol_types: List[ProtocolType]
    standards: List[str]
    pdu_name: str
    key_technologies: List[str]


def get_osi_model() -> Dict[int, OSILayer]:
    return {
        7: OSILayer(
            number=7,
            name="Application",
            function="Interface between network and application software",
            protocols=["HTTP", "SMTP", "FTP", "DNS", "DHCP", "SNMP", "SSH"],
            protocol_types=[ProtocolType.APPLICATION],
            standards=["RFC 2616 (HTTP)", "RFC 5321 (SMTP)", "RFC 959 (FTP)"],
            pdu_name="Message",
            key_technologies=["Web browsers", "Email clients", "APIs"]
        ),
        6: OSILayer(
            number=6,
            name="Presentation",
            function="Data translation, encryption, compression",
            protocols=["SSL/TLS", "JPEG", "MPEG", "ASCII", "Unicode"],
            protocol_types=[ProtocolType.ENCRYPTION, ProtocolType.DATA_FORMAT],
            standards=["RFC 8446 (TLS 1.3)", "ISO/IEC 10918 (JPEG)", "X.216"],
            pdu_name="Payload",
            key_technologies=["Encryption algorithms", "Compression formats"]
        ),
        5: OSILayer(
            number=5,
            name="Session",
            function="Manages connections between applications",
            protocols=["NetBIOS", "RPC", "PPTP", "SIP"],
            protocol_types=[ProtocolType.APPLICATION],
            standards=["RFC 1001/1002 (NetBIOS)", "RFC 5531 (RPC)", "RFC 2637 (PPTP)"],
            pdu_name="Session Data",
            key_technologies=["Session establishment", "Maintenance", "Termination"]
        ),
        4: OSILayer(
            number=4,
            name="Transport",
            function="End-to-end message delivery, error correction",
            protocols=["TCP", "UDP", "SCTP", "DCCP"],
            protocol_types=[ProtocolType.TRANSPORT],
            standards=["RFC 793 (TCP)", "RFC 768 (UDP)", "ISO/IEC 8073"],
            pdu_name="Segment (TCP) / Datagram (UDP)",
            key_technologies=["Port numbers", "Flow control", "Congestion avoidance"]
        ),
        3: OSILayer(
            number=3,
            name="Network",
            function="Logical addressing and routing",
            protocols=["IP", "ICMP", "OSPF", "BGP", "ARP", "IPsec"],
            protocol_types=[ProtocolType.ROUTING],
            standards=["RFC 791 (IPv4)", "RFC 8200 (IPv6)", "ISO/IEC 8208"],
            pdu_name="Packet",
            key_technologies=["Routers", "IP addressing", "Routing tables"]
        ),
        2: OSILayer(
            number=2,
            name="Data Link",
            function="Physical addressing and media access",
            protocols=["Ethernet", "PPP", "MAC", "VLAN", "LLC"],
            protocol_types=[ProtocolType.DATA_FORMAT],
            standards=["IEEE 802.3 (Ethernet)", "RFC 1661 (PPP)", "IEEE 802.1Q (VLAN)"],
            pdu_name="Frame",
            key_technologies=["Switches", "MAC addresses", "Error detection"]
        ),
        1: OSILayer(
            number=1,
            name="Physical",
            function="Transmits raw bit stream over physical medium",
            protocols=["100BASE-TX", "1000BASE-T", "DSL", "SONET", "Wi-Fi"],
            protocol_types=[],
            standards=["IEEE 802.3", "ITU-T G.992.x (DSL)", "IEEE 802.11 (Wi-Fi)"],
            pdu_name="Bit",
            key_technologies=["Cables", "Connectors", "NICs", "Hubs", "Repeaters"]
        ),
    }


def display_layer(layer_num: int, detailed: bool = False) -> None:
    model = get_osi_model()
    if layer_num not in model:
        print(f"Invalid layer number: {layer_num}. Must be 1–7.")
        return

    layer = model[layer_num]
    print(f"\n=== Layer {layer.number}: {layer.name} ===")
    print(f"\nPrimary Function: {layer.function}")
    print(f"\nProtocol Data Unit (PDU): {layer.pdu_name}")

    print("\nKey Protocols:")
    for proto in layer.protocols:
        std = next((s for s in layer.standards if proto in s), "No specific standard listed")
        print(f"  • {proto} — {std}")

    if detailed:
        print("\nKey Technologies:")
        for tech in layer.key_technologies:
            print(f"  • {tech}")

        print("\nTechnical Standards:")
        for std in layer.standards:
            print(f"  • {std}")


def list_layers(filter_type: Optional[ProtocolType] = None) -> None:
    model = get_osi_model()
    print("\nOSI Model Layers:")
    print("----------------")

    for num in sorted(model.keys()):
        layer = model[num]
        if filter_type and filter_type not in layer.protocol_types:
            continue

        func_summary = (layer.function[:60] + "...") if len(layer.function) > 60 else layer.function
        print(f"\nLayer {layer.number}: {layer.name}")
        print(f"  Function: {func_summary}")
        print(f"  Key Protocols: {', '.join(layer.protocols[:3])}{'...' if len(layer.protocols) > 3 else ''}")


def search_protocol(protocol: str) -> None:
    model = get_osi_model()
    found = False

    print(f"\nSearch Results for '{protocol.upper()}':")
    print("--------------------------------")

    for num in sorted(model.keys()):
        layer = model[num]
        matches = [p for p in layer.protocols if protocol.upper() in p.upper()]

        if matches:
            print(f"\nLayer {layer.number}: {layer.name}")
            print(f"  Protocols: {', '.join(matches)}")
            if layer.standards:
                print("  Standards:")
                for std in layer.standards:
                    print(f"    • {std}")
            found = True

    if not found:
        print(f"No protocols found matching '{protocol}'.")


def main():
    parser = argparse.ArgumentParser(
        description="OSI Model Reference Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  Show layer details:   %(prog)s -l 4
  List all layers:      %(prog)s --list
  Search for protocol:  %(prog)s -s TCP
  Detailed view:        %(prog)s -l 7 -d"""
    )

    parser.add_argument(
        "-l", "--layer",
        type=int,
        choices=range(1, 8),
        help="Display specific layer (1–7)"
    )
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Show detailed technical information"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all layers"
    )
    parser.add_argument(
        "-s", "--search",
        type=str,
        help="Search for protocol across all layers"
    )

    args = parser.parse_args()

    if args.layer:
        display_layer(args.layer, args.detailed)
    elif args.search:
        search_protocol(args.search)
    elif args.list:
        list_layers()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
