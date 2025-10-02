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