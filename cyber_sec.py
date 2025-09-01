# Import the socket module, which is necessary for all network-related operations.
import socket
import sys
import threading
from queue import Queue
TARGET_HOST = "localhost"
PORT_RANGE_START = 1
PORT_RANGE_END = 1024

# A simple banner to make the output more readable.
def print_banner():
    """Prints a friendly banner to the terminal."""
    print("-" * 50)
    print("      Simple Network Port Scanner")
    print("-" * 50)

def port_scanner(port):
"""
Attempts to connect to a specific port on the target host.
If the connection is successful, the port is considered open.
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)  # Set a timeout for the connection attempt.

try:
    # The connect_ex() method returns an error code instead of raising an exception.
    # This is ideal for scanning, as it doesn't halt the program on a closed port.
    conn = s.connect_ex((TARGET_HOST, port))
    
    # If the connection code is 0, the connection was successful, and the port is open.
    if conn == 0:
        print(f"Port {port}: OPEN")