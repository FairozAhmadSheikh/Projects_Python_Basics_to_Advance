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

def discover_network(cidr: str, use_arp_first=True) -> List[Dict]:
    
    results = []
    if SCAPY_AVAILABLE and use_arp_first:
        try:
            arp = arp_scan(cidr)
            # Convert to results with alive True
            for r in arp:
                results.append({"ip": r["ip"], "mac": r.get("mac"), "alive": True})
            return results
        except RuntimeError as e:
            print("[!] ARP scan failed or not permitted:", str(e))
    # Fallback to ping sweep (fast threaded)
    print("[+] Starting ping sweep (fallback)...")
    net = ipaddress.ip_network(cidr, strict=False)
    ip_list = [str(ip) for ip in net.hosts()]
    alive = []

    def _probe(ipaddr):
        if ping_host(ipaddr, timeout=0.8):
            return ipaddr
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
        futures = {ex.submit(_probe, ipaddr): ipaddr for ipaddr in ip_list}
        for fut in concurrent.futures.as_completed(futures):
            ipaddr = futures[fut]
            try:
                res = fut.result()
                if res:
                    alive.append(res)
            except Exception:
                continue
    results = [{"ip": ip, "mac": None, "alive": True} for ip in alive]
    return results


def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, Optional[str]]:
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((host, port))
            except Exception:
                return (port, False, None)
            # If connected, try to receive a small banner
            banner = None
            try:
                s.settimeout(0.8)
                banner = s.recv(1024).decode(errors="ignore").strip()
                if banner == "":
                    banner = None
            except Exception:
                banner = None
            return (port, True, banner)
    except Exception:
        return (port, False, None)

def scan_ports(host: str, ports: List[int], max_workers: int = 200) -> List[Dict]:
    
    results = []
    st = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_workers, len(ports) or 1)) as ex:
        futures = {ex.submit(scan_port, host, p): p for p in ports}
        for fut in concurrent.futures.as_completed(futures):
            try:
                port, is_open, banner = fut.result()
                results.append({"port": port, "open": is_open, "banner": banner})
            except Exception:
                p = futures[fut]
                results.append({"port": p, "open": False, "banner": None})
    results.sort(key=lambda x: x["port"])
    elapsed = time.time() - st
    print(f"[+] Scanned {len(ports)} ports on {host} in {elapsed:.2f}s")
    return results



def inspect_tls_cert(host: str, port: int = 443, timeout: float = 3.0) -> Dict:
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    info = {"host": host, "port": port, "error": None}
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                # cert is a dict per ssl.getpeercert()
                info["subject"] = dict(x[0] for x in cert.get("subject", ()))
                info["issuer"] = dict(x[0] for x in cert.get("issuer", ()))
                info["notAfter"] = cert.get("notAfter")
                info["notBefore"] = cert.get("notBefore")
                info["subjectAltName"] = cert.get("subjectAltName", ())
                # compute days left
                try:
                    notAfter = datetime.strptime(info["notAfter"], "%b %d %H:%M:%S %Y %Z")
                    info["days_left"] = (notAfter - datetime.utcnow()).days
                except Exception:
                    info["days_left"] = None
                # signature algorithm detection is not directly available from getpeercert
                info["raw_cert"] = cert
    except Exception as e:
        info["error"] = str(e)
    return info



def check_http_headers(host: str, port: int = 443, path: str = "/", timeout: float = 6.0) -> Dict:
    
    result = {"host": host, "port": port, "headers": {}, "secure": False, "error": None}
    url = f"https://{host}:{port}{path}"
    try:
        if REQUESTS_AVAILABLE:
            resp = requests.get(url, timeout=timeout, verify=False)
            result["status_code"] = resp.status_code
            headers = {k.lower(): v for k, v in resp.headers.items()}
            result["headers"] = headers
        else:
            # Raw HTTPS GET using ssl-wrapped socket (simple)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with socket.create_connection((host, port), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\nUser-Agent: SecToolbox/1.0\r\n\r\n"
                    ssock.send(req.encode())
                    data = b""
                    while True:
                        chunk = ssock.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                    head, _, _ = data.partition(b"\r\n\r\n")
                    headers_raw = head.decode(errors="ignore").split("\r\n")[1:]
                    headers = {}
                    for line in headers_raw:
                        if ":" in line:
                            k, v = line.split(":", 1)
                            headers[k.strip().lower()] = v.strip()
                    result["headers"] = headers
        # Check some security headers
        headers = result["headers"]
        sec_checks = {
            "hsts": "strict-transport-security" in headers,
            "csp": "content-security-policy" in headers,
            "x_frame": "x-frame-options" in headers,
            "x_xss": "x-xss-protection" in headers,
            "referrer_policy": "referrer-policy" in headers,
            "content_type_options": "x-content-type-options" in headers,
        }
        result["security_headers_present"] = sec_checks
        result["secure"] = True
    except Exception as e:
        result["error"] = str(e)
    return result



def save_report_json(report: Dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"[+] Report saved to {filename}")


MENU = """
SecToolbox - Choose an option:
1) Discover local network (CIDR) (ARP/ping)
2) Scan ports on host
3) Inspect TLS certificate of host
4) Check HTTP security headers
5) Full host quick-check (port scan + cert + headers)
6) Save last report to JSON
7) Quit
"""

def full_host_check(host: str, ports: List[int]) -> Dict:
    
    report = {"host": host, "timestamp": now_ts()}
    # check liveness
    alive = ping_host(host, timeout=1.2)
    report["alive"] = alive
    # ports
    port_scan_result = scan_ports(host, ports, max_workers=200)
    report["ports"] = port_scan_result
    # TLS
    tls_info = inspect_tls_cert(host, port=443)
    report["tls"] = tls_info
    # headers
    http_headers = check_http_headers(host, port=443)
    report["http"] = http_headers
    # simple suggestions
    suggestions = []
    if tls_info.get("error"):
        suggestions.append("TLS handshake failed or invalid certificate.")
    else:
        days = tls_info.get("days_left")
        if days is not None and days < 30:
            suggestions.append(f"Certificate expires in {days} days — consider renewal.")
    # header suggestions
    headers = http_headers.get("headers", {})
    if "strict-transport-security" not in headers:
        suggestions.append("Missing Strict-Transport-Security header; enable HSTS for HTTPS sites.")
    if "content-security-policy" not in headers:
        suggestions.append("Missing Content-Security-Policy; consider adding to mitigate XSS.")
    report["suggestions"] = suggestions
    return report

def interactive_menu():
    last_report = None
    while True:
        print(MENU)
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            cidr = input("Enter network CIDR (eg. 192.168.1.0/24): ").strip()
            if not confirm_authorization():
                print("Authorization not confirmed. Aborting discovery.")
                continue
            try:
                res = discover_network(cidr)
                print(f"Discovered {len(res)} live hosts:")
                for r in res:
                    print(f" - {r['ip']}  MAC: {r.get('mac') or 'unknown'}")
                last_report = {"action": "discover", "cidr": cidr, "results": res, "ts": now_ts()}
            except Exception as e:
                print("[!] Discovery failed:", e)
        elif choice == "2":
            host = input("Enter host/IP to scan: ").strip()
            if not confirm_authorization():
                print("Authorization not confirmed. Aborting scan.")
                continue
            ports_in = input("Enter ports (eg. 22,80,443 or 1-1024): ").strip() or "1-1024"
            ports = parse_ports(ports_in)
            print(f"[+] Scanning {host} ports: {ports_in} (total {len(ports)})")
            res = scan_ports(host, ports)
            for r in res:
                if r["open"]:
                    print(f"[OPEN] {r['port']:5}  banner: {r['banner'] or '<none>'}")
            last_report = {"action": "port_scan", "host": host, "ports": ports, "results": res, "ts": now_ts()}
        elif choice == "3":
            host = input("Enter hostname for TLS inspect (eg. example.com): ").strip()
            info = inspect_tls_cert(host, 443)
            if info.get("error"):
                print("[!] TLS inspect error:", info["error"])
            else:
                print("[+] Certificate subject:", info.get("subject"))
                print("[+] Issuer:", info.get("issuer"))
                print("[+] NotBefore:", info.get("notBefore"))
                print("[+] NotAfter:", info.get("notAfter"))
                print("[+] Days left:", info.get("days_left"))
            last_report = {"action": "tls_inspect", "host": host, "info": info, "ts": now_ts()}
        elif choice == "4":
            host = input("Enter hostname for HTTP header check (eg. example.com): ").strip()
            res = check_http_headers(host, 443)
            if res.get("error"):
                print("[!] HTTP check failed:", res["error"])
            else:
                print(f"[+] Status code: {res.get('status_code', '<unknown>')}")
                print("[+] Security header presence:")
                for k, v in res.get("security_headers_present", {}).items():
                    print(f"  - {k}: {'present' if v else 'missing'}")
            last_report = {"action": "http_headers", "host": host, "result": res, "ts": now_ts()}
        elif choice == "5":
            host = input("Host/IP for full quick-check: ").strip()
            if not confirm_authorization():
                print("Authorization not confirmed. Aborting full check.")
                continue
            ports_in = input("Which ports to scan? (eg 22,80,443 or 1-1024) [default: 22,80,443]: ").strip() or "22,80,443"
            ports = parse_ports(ports_in)
            report = full_host_check(host, ports)
            # Print summary
            print(f"=== Quick-check report for {host} ===")
            print("Alive:", report["alive"])
            open_ports = [x["port"] for x in report["ports"] if x["open"]]
            print("Open ports:", open_ports or "None")
            if report["tls"].get("error"):
                print("TLS: error -", report["tls"]["error"])
            else:
                print("TLS NotAfter:", report["tls"].get("notAfter"), "Days left:", report["tls"].get("days_left"))
            print("HTTP security headers present:")
            for k, v in report["http"].get("security_headers_present", {}).items():
                print(f" - {k}: {'present' if v else 'missing'}")
            if report["suggestions"]:
                print("Suggested actions:")
                for s in report["suggestions"]:
                    print(" -", s)
            last_report = report
        elif choice == "6":
            if last_report is None:
                print("No report to save.")
            else:
                fn = input("Filename to save JSON report [default: sectool_report.json]: ").strip() or "sectool_report.json"
                save_report_json(last_report, fn)
        elif choice == "7":
            print("Bye.")
            break
        else:
            print("Invalid selection. Choose 1-7.")
