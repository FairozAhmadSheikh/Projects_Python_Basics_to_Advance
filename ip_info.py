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
def display_ip_info(ip_address):
    try:
        # Replace with your actual ipinfo API token
        access_token = 'YOUR_API_TOKEN_HERE' 
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip_address)

        if details:
            print("\n✨ That's a cool IP! Here's what I found about it: ✨")
            print(f"🌎 Location: {details.city}, {details.region}, {details.country_name}")
            print(f"🗺️ Coordinates: {details.latitude}, {details.longitude}")
            print(f"📡 Internet Service Provider: {details.org}")
            print(f"🕰️ Timezone: {details.timezone}")
            print(f"💻 Hostname: {details.hostname}")
        else:
            print("Couldn't retrieve detailed information for that IP.")
    except Exception as e:
        print(f"An error occurred while retrieving IP details: {e}")