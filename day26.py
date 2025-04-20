#pip install reportlab

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_invoice(customer_name, items, filename="invoice.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(50, height - 100, f"Billed To: {customer_name}")

    # Table header
    c.drawString(50, height - 140, "Item")
    c.drawString(250, height - 140, "Quantity")
    c.drawString(350, height - 140, "Price")
    c.drawString(450, height - 140, "Total")
