from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def send_invoice_email(to_email: str, filepath: str):
    message = MessageSchema(
        subject="Your UKSChat Subscription Invoice",
        recipients=[to_email],
        body="Thank you for your purchase! Your invoice is attached.",
        attachments=[filepath],
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
