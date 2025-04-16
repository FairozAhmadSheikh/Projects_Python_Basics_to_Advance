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