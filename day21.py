# pip install geocoder folium tk
import tkinter as tk
import geocoder
import folium
import webbrowser
import os
import threading
import time

class LocationTracker:
    def __init__(self, update_interval=10):
        self.update_interval = update_interval
        self.running = False
        self.map_file = "live_location.html"

    def get_location(self):
        g = geocoder.ip('me')
        return g.latlng

    def update_map(self):
        latlng = self.get_location()
        if latlng:
            m = folium.Map(location=latlng, zoom_start=15)
            folium.Marker(latlng, tooltip="You are here").add_to(m)
            m.save(self.map_file)
            webbrowser.open('file://' + os.path.realpath(self.map_file))

    def start_tracking(self):
        self.running = True
        def track():
            while self.running:
                self.update_map()
                time.sleep(self.update_interval)
        threading.Thread(target=track, daemon=True).start()

    def stop_tracking(self):
        self.running = False
# ---------- GUI ----------
def main():
    tracker = LocationTracker()

    root = tk.Tk()
    root.title("📍 Real-Time Location Tracker")
    root.geometry("300x180")

    tk.Label(root, text="Track your IP-based location", font=("Arial", 12)).pack(pady=10)

    def start():
        status_label.config(text="Tracking started...")
        tracker.start_tracking()

    def stop():
        tracker.stop_tracking()
        status_label.config(text="Tracking stopped.")