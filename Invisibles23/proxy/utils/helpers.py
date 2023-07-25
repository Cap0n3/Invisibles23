import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import environ
from Invisibles23.settings import BASE_DIR

# Read the environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

CURR_PATH = os.path.dirname(os.path.realpath(__file__))

def sendEmail(name, email):
    # Email configuration
    sender_email = 'webmaster@blackwidowsproject.ch'
    sender_password = env('INFOMANIAK_EMAIL_PASSWORD')
    receiver_email = 'cap0n3@protonmail.com' # For testing purposes
    subject = "Adhésion à l'association Les Invisibles"
    
    with open(f"{CURR_PATH}/adhesion_email.html", "r") as f:
        html_content = f.read()
    
    # Replace the {name} placeholder with the actual customer name
    html_content = html_content.replace('{name}', name)

    # Create a MIMEText object for HTML content
    html_part = MIMEText(html_content, 'html')

    # Create a MIMEText object to represent the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the HTML part to the message
    message.attach(html_part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('mail.infomaniak.com', 587) as server:
        server.starttls()  # Enable encryption
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
