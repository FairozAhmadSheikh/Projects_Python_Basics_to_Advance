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
except socket.gaierror:
        # Handles errors related to an invalid hostname.
        print("Hostname could not be resolved. Exiting.")
        sys.exit()
    except socket.error:
        # Handles generic socket errors.
        print("Could not connect to the server.")
        sys.exit()
    finally:
        # Always close the socket to free up system resources.
        s.close()
if __name__ == "__main__":
    print_banner()

    target_input = input("Enter the target host to scan: ").strip()
        if target_input:
            TARGET_HOST = target_input
    while True:
        try:
            port_start_input = int(input("Enter the starting port: ").strip())
            port_end_input = int(input("Enter the ending port: ").strip())
            
            # Validate the port range.
            if 0 <= port_start_input <= 65535 and 0 <= port_end_input <= 65535 and port_start_input <= port_end_input:
                PORT_RANGE_START = port_start_input
                PORT_RANGE_END = port_end_input
                break
            else:
                print("Invalid port range. Ports must be between 0 and 65535, and the start port must be less than or equal to the end port.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

            print(f"\nScanning host: {TARGET_HOST}")
            print(f"Scanning port range: {PORT_RANGE_START} - {PORT_RANGE_END}\n")

            # This loop iterates through the specified port range and calls the scanner function for each port.
            try:
                for port in range(PORT_RANGE_START, PORT_RANGE_END + 1):
                    port_scanner(port)
                    
            except KeyboardInterrupt:
                # Allows the user to gracefully exit the program by pressing Ctrl+C.
                print("\nScan interrupted by user. Exiting.")
                sys.exit()