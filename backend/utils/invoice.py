from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

def generate_invoice(payment, user, plan):
    invoice_dir = "invoices"
    os.makedirs(invoice_dir, exist_ok=True)

    filename = f"invoice_{payment.id}.pdf"
    filepath = os.path.join(invoice_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "UKSChat - Invoice")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Invoice ID : {payment.id}")
    c.drawString(50, 750, f"User Email: {user.email}")
    c.drawString(50, 730, f"Plan: {plan.name}")
    c.drawString(50, 710, f"Amount: {plan.currency} {plan.price:.2f}")
    c.drawString(50, 690, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

    c.drawString(50, 650, "Thank you for your purchase!")
    c.drawString(50, 630, "Enjoy priority AI access")

    c.showPage()
    c.save()

    return filename, filepath
