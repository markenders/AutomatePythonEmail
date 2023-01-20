from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv
from datetime import date
import ssl
import smtplib
import os

# load .env vars
load_dotenv()

email_sender = 'themarkenders@gmail.com'
email_password = os.getenv('SOME_SECRET')

# get today's date
today = date.today()
# get day name in english
date = today.strftime("%B %d, %Y")

num = 0
quotes = [
    "“All our dreams can come true, if we have the courage to pursue them.” —Walt Disney", "quote 2"]


def send_email(Name, email_receiver):
    em = EmailMessage()
    em['From'] = formataddr(("Daily QOTD", f"{email_sender}"))
    em['To'] = email_receiver

    # Set the subject and body of the email
    em['Subject'] = 'Good morning! For ' + date

    em.set_content(
        f"""\
        Hello {Name},
        
        Quote of the day: {quotes[num]}

        Have a great day!
        """
    )
    em.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hello {Name},</p>
        <p>Quote of the day: {quotes[num]}</p>
        <p>Have a great day!</p>
      </body>
    </html>
    """,
        subtype="html",
    )

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
