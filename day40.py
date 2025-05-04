import socket
import threading
from colorama import Fore, Style

# Common ports and services
common_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-ALT"
}
open_ports = []

def scan_port(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        service = common_ports.get(port, "Unknown")
        print(f"{Fore.GREEN}[+] Port {port} OPEN ({service}){Style.RESET_ALL}")
        open_ports.append((port, service))
        sock.close()
    except:
        pass
def main():
    target = input("🔍 Enter target IP address: ").strip()
    start_port = int(input("🔢 Start port: "))
    end_port = int(input("🔢 End port: "))
    print(f"\n🕵️ Scanning {target} from port {start_port} to {end_port}...\n")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("\n✅ Scan Complete.")
    if open_ports:
        print("📄 Open Ports:")
        for port, service in open_ports:
            print(f" - {port} ({service})")
    else:
        print("❌ No open ports found.")
c6