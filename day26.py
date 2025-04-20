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
    y = height - 160
    grand_total = 0

    for item in items:
        name, qty, price = item
        total = qty * price
        grand_total += total

        c.drawString(50, y, name)
        c.drawString(250, y, str(qty))
        c.drawString(350, y, f"${price:.2f}")
        c.drawString(450, y, f"${total:.2f}")
        y -= 20
    # Total
    tax = 0.18 * grand_total
    final_total = grand_total + tax

    c.drawString(50, y - 20, f"Subtotal: ${grand_total:.2f}")
    c.drawString(50, y - 40, f"Tax (18%): ${tax:.2f}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 70, f"Total Amount: ${final_total:.2f}")

    c.save()
    print(f"✅ Invoice saved as {filename}")

# Example usage
customer = "Mohammed Hussain Malik"
items = [
    ("Python Training", 2, 1500),
    ("AI Bootcamp", 1, 2500),
    ("Machine Learning Notes", 3, 500),
]