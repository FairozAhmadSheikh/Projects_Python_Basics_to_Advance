import requests  # for making HTTP requests
import time      # for simulating loading delays
import sys       # for terminal animations
import textwrap  # for wrapping long text


# function to create a typing animation
def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
# function to display a simple loading spinner
def loading_animation(message="Fetching data"):
    animation = "|/-\\"
    for i in range(20):
        time.sleep(0.1)
        sys.stdout.write(f"\r{message} " + animation[i % len(animation)])
        sys.stdout.flush()
    print("\r", end="")

# function to fetch random astronomy data (no API key required)
def fetch_space_data():
    # we are using a public mirror of NASA's APOD API
    url = "https://api.npoint.io/8d51a3c45b29d55bf6c3"  # this contains sample APOD entries
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return []
    except Exception as e:
        print("Error while fetching data:", e)
        return []
# function to nicely display the astronomy facts
def display_fact(fact):
    print("\n" + "="*60)
    slow_print(f"🌠  {fact['title']}")
    print("="*60)
    print(f" Date: {fact['date']}\n")

    wrapped_text = textwrap.fill(fact['explanation'], width=70)
    slow_print(wrapped_text)
    
    print("\n Image URL:", fact['url'])
    print("="*60 + "\n")
# main CLI interface
def main():
    slow_print("🚀 Welcome to SPACE EXPLORER CLI 🌌")
    slow_print("Fetching random astronomy facts from NASA’s archive...\n")
    
    loading_animation()
    data = fetch_space_data()
    
    if not data:
        print("No data available. Try again later.")
        return
    