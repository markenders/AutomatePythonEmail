from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv
from datetime import date
from Quotes import quotes
import ssl
import smtplib
import os
import random

# load .env vars
load_dotenv()

email_sender = 'themarkenders@gmail.com'
email_password = os.getenv('SOME_SECRET')

# get today's date
today = date.today()
# get day name in english
date = today.strftime("%B %d, %Y")

# get index from quotecounter


def getQuoteIndex(filename="quotecounter.txt"):
    with open(filename, "a+") as getIndex:
        getIndex.seek(0)

        val = int(getIndex.read() or 0)+1

        # end of loop/quote index reset to 1
        if (val >= len(quotes)):
            val = 1

        getIndex.seek(0)
        getIndex.truncate()
        getIndex.write(str(val))
        return val


# What index of quotes[] is on
dailyIndex = getQuoteIndex()


def send_email(Name, email_receiver):
    em = EmailMessage()
    em['From'] = formataddr(("QOTD", f"{email_sender}"))
    em['To'] = email_receiver

    # gives somebody a default name randomly
    defaultName = ["King", "Monkey", "Buns", "Queen", "Nooblet", "Panda", "Smooshie", "Luigi", "Captain America", "Gandalf", "Flippers", "Butters",
                   "Doofus", "Bambi", "Cinnamon", "Silly", "Billy", "Tarzan", "Kitty", "Pipsqueak",
                   "Mario", "Pikachu", "Sonic the Hedgehog", "Link", "Master Chief", "Donkey Kong", "Crash Bandicoot", "Zelda"]

    if (Name == None or Name == ''):
        Name = defaultName[random.randint(0, len(defaultName)-1)]

    # Set the subject and body of the email
    em['Subject'] = 'Good morning! For ' + date

    em.set_content(
        f"""\
    <html>
      <body>
        <p>Hello {Name},</p>
        <p>Quote of the day: {quotes[dailyIndex]}</p>
        <p>Have a great day!</p>
        <P>
        <p><a href="https://docs.google.com/forms/d/e/1FAIpQLSd4b6EuWVAGz0zhO4wNZT9Idv51nihRvH7E_IymAz4g11RscA/viewform">Unsubscribe</a></p>
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
