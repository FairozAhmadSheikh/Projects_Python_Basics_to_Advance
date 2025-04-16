"""
pip install pipwin  
pipwin install pyaudio

"""

import socket
import threading
from queue import Queue
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.CYAN + "🔍 Simple Port Scanner with Banner Grabbing")

target = input("Enter target IP or domain: ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))

thread_count = 100
queue = Queue()
def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((target, port))
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "No banner"
        print(Fore.GREEN + f"[+] Port {port} is OPEN → {banner}")
        s.close()
    except:
        pass
def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()
def main():
    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    queue.join()
    print(Fore.CYAN + "\n✅ Scan complete.")
if __name__ == "__main__":
    main()