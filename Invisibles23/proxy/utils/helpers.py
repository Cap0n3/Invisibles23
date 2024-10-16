import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import environ
from Invisibles23.settings import BASE_DIR
from Invisibles23.logging_config import logger
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime

# Read the environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

CURR_PATH = os.path.dirname(os.path.realpath(__file__))


def sendEmail(receiver_email, subject, email_file, placeholders={}) -> None:
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
    logger.info(f"Sending email to {receiver_email}...")
    try:
        sender_email = env("OWNER_EMAIL")
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
                html_content = html_content.replace(
                    f"{{{key}}}", value if value is not None else "None"
                )

        # Create a MIMEText object for HTML content
        html_part = MIMEText(html_content, "html")

        # Attach the HTML part to the message
        message.attach(html_part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("mail.infomaniak.com", 587) as server:
            server.starttls()  # Enable encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        logger.error(f"An error occurred while sending the email: {e}")


def find_key_in_dict(d, target) -> str:
    """
    Recursively search for a key in a nested dictionary.

    Param
    ------
    d: dict
        The dictionary to search in
    target: str
        The key to search for, like "SECRET_KEY"

    Return
    ------
    The value of the key if found, None otherwise
    """
    if target in d:
        return d[target]
    for key, value in d.items():
        if isinstance(value, dict):
            result = find_key_in_dict(value, target)
            if result is not None:
                return result
    return None


def mailchimp_add_subscriber(
    mailchimp_api_key, server_prefix, list_id, member_info
) -> JsonResponse:
    """
    This function is used to add a subscriber to a Mailchimp list through the Mailchimp API.

    Parameters
    ----------
    mailchimp_api_key: str
        The Mailchimp API key
    server_prefix: str
        The server prefix of the Mailchimp API key (e.g. us9, us10, etc.)
    list_id: str
        The ID of the Mailchimp list to add the subscriber to
    member_info: dict
        A dictionary containing the information of the subscriber to add to the list

    Returns
    -------
    JsonResponse
        A JSON response containing the message of the operation
    """
    logger.info("Adding subscriber to Mailchimp list...")

    try:
        client = MailchimpMarketing.Client()
        client.set_config({"api_key": mailchimp_api_key, "server": server_prefix})
        response = client.lists.add_list_member(list_id, member_info)
        logger.info(f"Mailchimp response: {response}")

        return JsonResponse(
            {
                "message": "You have successfully subscribed to our mailing list.",
            },
            status=200,
        )
    except ApiClientError as error:
        logger.error(f"An exception occurred: {error.text}")

        return JsonResponse(
            {
                "message": f"An error occurred: {error.text}",
            },
            status=error.status_code,
        )


def format_birthdate_for_mailchimp(birthdate) -> str:
    """
    Format the birthdate to the required format for Mailchimp (mm/dd).
    If the birthdate is not in the correct format, it is set to an empty string.
    """
    formats = [
        "%Y-%m-%d",  # For format like 2024-12-01
        "%d-%m-%Y",  # For format like 31-12-2024
    ]

    for fmt in formats:
        try:
            date_obj = datetime.strptime(birthdate, fmt)
            return date_obj.strftime("%m/%d")
        except ValueError:
            continue

    logger.warning(f"Invalid birthdate format: {birthdate}")
    return ""
