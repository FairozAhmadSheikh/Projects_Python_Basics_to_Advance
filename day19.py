import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Image Editor")
        self.root.geometry("800x600")

        self.image = None
        self.img_label = tk.Label(root)
        self.img_label.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Open Image", command=self.open_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Grayscale", command=self.to_grayscale).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Blur", command=self.blur_image).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Rotate 90°", command=self.rotate_image).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Flip Horizontally", command=self.flip_image).grid(row=0, column=5, padx=5)