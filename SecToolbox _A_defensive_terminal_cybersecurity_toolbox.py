import argparse
import concurrent.futures
import ipaddress
import json
import socket
import ssl
import sys
import threading
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional

try:
    from scapy.all import ARP, Ether, srp, conf  # type: ignore
    SCAPY_AVAILABLE = True
except Exception:
    SCAPY_AVAILABLE = False

try:
    import requests  # type: ignore
    REQUESTS_AVAILABLE = True
except Exception:
    REQUESTS_AVAILABLE = False

def confirm_authorization() -> bool:
    
    print("\n=== AUTHORIZATION REQUIRED ===")
    print("You must have explicit authorization to scan the target(s).")
    resp = input("Type 'I have permission' to proceed, anything else to abort: ").strip()
    return resp.lower() == "i have permission"

def now_ts() -> str:
    return datetime.utcnow().isoformat() + "Z"

def parse_ports(ports_str: str) -> List[int]:
   
    ports = set()
    for part in ports_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
            ports.update(range(a, b+1))
        else:
            ports.add(int(part))
    return sorted(p for p in ports if 0 < p < 65536)
