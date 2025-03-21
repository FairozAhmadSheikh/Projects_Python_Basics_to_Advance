import tkinter as tk
import time

# def update_time():
#     """Update the clock display every second."""
    current_time = time.strftime("%H:%M:%S %p")
    label.config(text=current_time)
    label.after(1000, update_time)  # Update every 1 second

# Create the main window
root = tk.Tk()
root.title("Digital Clock")
root.configure(bg="black")

# Create the clock label
label = tk.Label(root, font=("Arial", 50, "bold"), bg="black", fg="cyan")
label.pack(padx=20, pady=20)

# Start the clock
update_time()

# Run the application
root.mainloop()
