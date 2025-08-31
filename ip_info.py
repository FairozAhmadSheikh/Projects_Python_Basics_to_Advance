import requests
import ipinfo


def get_user_ip():
    """Fetches the user's public IP address."""
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['ip']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None
