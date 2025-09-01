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