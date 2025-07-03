#!/usr/bin/env python3
"""
OSI Model Reference Tool

Provides detailed technical specifications for each layer of the OSI model,
including protocols, functions, and technical standards.
"""

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
    pdu_name: str  # Protocol Data Unit name
    key_technologies: str

def get_osi_model() -> Dict[int, OSILayer]:
    """Returns complete OSI model reference data"""
    return {
        7: OSILayer(
            number=7,
            name="Application",
            function="Interface between network and application software",
            protocols=["HTTP", "SMTP", "FTP", "DNS", "DHCP", "SNMP", "SSH"],
            protocol_types=[ProtocolType.APPLICATION],
            standards=["RFC 2616 (HTTP)", "RFC 5321 (SMTP)", "RFC 959 (FTP)"],
            pdu_name="Message",
            key_technologies="Web browsers, email clients, APIs"
        ),
        6: OSILayer(
            number=6,
            name="Presentation",
            function="Data translation, encryption, compression",
            protocols=["SSL/TLS", "JPEG", "MPEG", "ASCII", "Unicode"],
            protocol_types=[ProtocolType.ENCRYPTION, ProtocolType.DATA_FORMAT],
            standards=["RFC 8446 (TLS 1.3)", "ISO/IEC 10918 (JPEG)", "X.216"],
            pdu_name="Payload",
            key_technologies="Encryption algorithms, compression formats"
        ),
        5: OSILayer(
            number=5,
            name="Session",
            function="Manages connections between applications",
            protocols=["NetBIOS", "RPC", "PPTP", "SIP"],
            protocol_types=[ProtocolType.APPLICATION],
            standards=["RFC 1001/1002 (NetBIOS)", "RFC 5531 (RPC)", "RFC 2637 (PPTP)"],
            pdu_name="Session Data",
            key_technologies="Session establishment, maintenance, termination"
        ),
        4: OSILayer(
            number=4,
            name="Transport",
            function="End-to-end message delivery, error correction",
            protocols=["TCP", "UDP", "SCTP", "DCCP"],
            protocol_types=[ProtocolType.TRANSPORT],
            standards=["RFC 793 (TCP)", "RFC 768 (UDP)", "ISO/IEC 8073"],
            pdu_name="Segment (TCP) / Datagram (UDP)",
            key_technologies="Port numbers, flow control, congestion avoidance"
        ),
        3: OSILayer(
            number=3,
            name="Network",
            function="Logical addressing and routing",
            protocols=["IP", "ICMP", "OSPF", "BGP", "ARP", "IPsec"],
            protocol_types=[ProtocolType.ROUTING],
            standards=["RFC 791 (IPv4)", "RFC 8200 (IPv6)", "ISO/IEC 8208"],
            pdu_name="Packet",
            key_technologies="Routers, IP addressing, routing tables"
        ),
        2: OSILayer(
            number=2,
            name="Data Link",
            function="Physical addressing and media access",
            protocols=["Ethernet", "PPP", "MAC", "VLAN", "LLC"],
            protocol_types=[ProtocolType.DATA_FORMAT],
            standards=["IEEE 802.3 (Ethernet)", "RFC 1661 (PPP)", "IEEE 802.1Q (VLAN)"],
            pdu_name="Frame",
            key_technologies="Switches, MAC addresses, error detection"
        ),
        1: OSILayer(
            number=1,
            name="Physical",
            function="Transmits raw bit stream over physical medium",
            protocols=["100BASE-TX", "1000BASE-T", "DSL", "SONET", "Wi-Fi"],
            protocol_types=[],
            standards=["IEEE 802.3", "ITU-T G.992.x (DSL)", "IEEE 802.11 (Wi-Fi)"],
            pdu_name="Bit",
            key_technologies="Cables, connectors, NICs, hubs, repeaters"
        )
    }

def display_layer(layer_num: int, detailed: bool = False) -> None:
    """Display detailed information about a specific OSI layer"""
    model = get_osi_model()
    if layer_num not in model:
        print(f"Invalid layer number: {layer_num}. Must be 1-7.")
        return
    
    layer = model[layer_num]
    print(f"\n=== Layer {layer.number}: {layer.name} ===")
    print(f"\nPrimary Function: {layer.function}")
    print(f"\nProtocol Data Unit (PDU): {layer.pdu_name}")
    
    print("\nKey Protocols:")
    for proto, std in zip(layer.protocols, layer.standards):
        print(f"  • {proto.ljust(8)} ({std})")
    
    if detailed:
        print("\nKey Technologies:")
        print(f"  {layer.key_technologies}")
        
        print("\nTechnical Standards:")
        for std in layer.standards:
            print(f"  • {std}")

def list_layers(filter_type: Optional[ProtocolType] = None) -> None:
    """List all OSI layers with optional filtering"""
    model = get_osi_model()
    print("\nOSI Model Layers:")
    print("----------------")
    
    for num in sorted(model.keys()):
        layer = model[num]
        if filter_type and filter_type not in layer.protocol_types:
            continue
            
        print(f"\nLayer {layer.number}: {layer.name}")
        print(f"  Function: {layer.function.split('.')[0]}...")
        print(f"  Key Protocols: {', '.join(layer.protocols[:3])}...")

def search_protocol(protocol: str) -> None:
    """Search for a protocol across all layers"""
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
            print(f"  Standards: {layer.standards[0]}")
            found = True
    
    if not found:
        print(f"No protocols found matching '{protocol}'")

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
        help="Display specific layer (1-7)"
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
