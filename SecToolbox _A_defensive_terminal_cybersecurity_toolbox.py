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

def arp_scan(network_cidr: str, timeout: float = 2.0) -> List[Dict]:
    
    if not SCAPY_AVAILABLE:
        raise RuntimeError("scapy not available for ARP scan.")
    conf.verb = 0
    print(f"[+] Starting ARP scan on {network_cidr} (this may require root)...")
    net = str(network_cidr)
    try:
        arp = ARP(pdst=net)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        ans, _ = srp(packet, timeout=timeout, retry=1)
        results = []
        for s, r in ans:
            results.append({"ip": r.psrc, "mac": r.hwsrc})
        return results
    except PermissionError:
        raise RuntimeError("Permission denied: ARP scan requires root privileges.")

def ping_host(ip: str, timeout: float = 1.0) -> bool:
    
    try:
        # Quick TCP probe to port 80 and 443 as liveness indicator
        for port in (80, 443):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                try:
                    s.connect((ip, port))
                    return True
                except Exception:
                    continue
    except Exception:
        pass
    # As last resort, try system ping
    import subprocess, platform
    param = "-n" if platform.system().lower()=="windows" else "-c"
    cmd = ["ping", param, "1", "-W", str(int(timeout)), ip]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False
