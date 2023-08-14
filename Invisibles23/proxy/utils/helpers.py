import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import environ
from Invisibles23.settings import BASE_DIR

# Read the environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

CURR_PATH = os.path.dirname(os.path.realpath(__file__))

def sendEmail(receiver_email, subject, email_file, placeholders={}):
    """
    Send an email to the given receiver email address. The email file is an HTML file that contains the email content. 
    The placeholders in the email file are replaced with the actual values.

    Param
    ------
    receiver_email: str
        The email address of the receiver
    subject: str
        The subject of the email
    email_file: str
        The name of the email file to send
    placeholders: dict
        A dictionary of placeholders and their values
    """
    sender_email = "association@lesinvisibles.ch"
    sender_password = env("INFOMANIAK_EMAIL_PASSWORD")

    # Create a MIMEText object to represent the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Read the email file
    with open(f"{CURR_PATH}/email_templates/{email_file}", "r") as f:
        html_content = f.read()

    # Replace the placeholders in email with the actual values
    if len(placeholders) != 0:
        for key, value in placeholders.items():
            html_content = html_content.replace(f"{{{key}}}", value)

    # Create a MIMEText object for HTML content
    html_part = MIMEText(html_content, "html")
    
    # Attach the HTML part to the message
    message.attach(html_part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("mail.infomaniak.com", 587) as server:
        server.starttls()  # Enable encryption
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())