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

def sendEmailToOwner(fname, lname, email, message):
    try:
        # Email configuration
        sender_email = "association@lesinvisibles.ch"
        sender_password = env("INFOMANIAK_EMAIL_PASSWORD")
        receiver_email = "association@lesinvisibles.ch"
        subject = "Nouveau message depuis le site web"

        with open(f"{CURR_PATH}/contact_email.html", "r") as f:
            html_content = f.read()

        print(fname, lname, email, message)
        # Replace the {fame} {lname} {email} placeholder in the html
        html_content = html_content.replace("{fname}", fname)
        html_content = html_content.replace("{lname}", lname)
        html_content = html_content.replace("{email}", email)
        html_content = html_content.replace("{message}", message)

        # Create a MIMEText object for HTML content
        html_part = MIMEText(html_content, "html")

        # Create a MIMEText object to represent the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the HTML part to the message
        message.attach(html_part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("mail.infomaniak.com", 587) as server:
            server.starttls()  # Enable encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
        return False
    else:
        print("Email sent successfully")
        return True


def sendEmailToMember(name, email):
    # Email configuration
    sender_email = "association@lesinvisibles.ch"
    sender_password = env("INFOMANIAK_EMAIL_PASSWORD")
    receiver_email = email
    subject = "Adhésion à l'association Les Invisibles"

    with open(f"{CURR_PATH}/adhesion_email.html", "r") as f:
        html_content = f.read()

    # Replace the {name} placeholder with the actual customer name
    html_content = html_content.replace("{name}", name)

    # Create a MIMEText object for HTML content
    html_part = MIMEText(html_content, "html")

    # Create a MIMEText object to represent the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the HTML part to the message
    message.attach(html_part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("mail.infomaniak.com", 587) as server:
        server.starttls()  # Enable encryption
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
