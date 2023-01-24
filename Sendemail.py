from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv
from datetime import date
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


def getQuoteIndex(filename="quotecounter.txt"):
    with open(filename, "a+") as getIndex:
        getIndex.seek(0)
        val = int(getIndex.read() or 0)+1
        getIndex.seek(0)
        getIndex.truncate()
        getIndex.write(str(val))
        return val


dailyIndex = getQuoteIndex()

quotes = [
    "Blank",
    "“All our dreams can come true, if we have the courage to pursue them.” —Walt Disney",
    "“If you have the opportunity to play this game called life, you have to appreciate every moment. A lot of people don't appreciate their moment until it's passed” —Kanye West",
    "“You’re the smartest guy I’ve ever met. And you’re too stupid to see… he made up his mind ten minutes ago.” —Hank Schrader from Breaking Bad",
    "“You are trouble. I’m sorry the kid here doesn’t see it, but I sure as hell do. You are a time bomb. Tick tick ticking. And I have no intention for being around for the boom.” —Mike Ehrmantraut from Breaking Bad",
    "“Hate. A little bit's okay. As long as you never forget who's boss.” —Don Eladio Vuente from Better Call Saul",
    "“I am the danger. A guy opens his door and gets shot, and you think that of me? No... I am the one who knocks!” —Walter White from Breaking Bad",
    "“Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me.” —Michael Scott from The Office",
    "“There’s a lot of beauty in ordinary things. Isn’t that kind of the point?” —Pam Beesly from The Office",
    "“I wish there was a way to know you're in the good old days before you've actually left them.” —Andy Bernard from The Office",
    "“I'm not superstitious but I'm a little stitious.” —Michael Scott from The Office",
    "“People underestimate the power of nostalgia. Nostalgia is truly one of the greatest human weaknesses... second only to the neck.” —Dwight Schrute from The Office",
    "“I was everyone I'd ever met who I never loved enough” —Robert DeLong",
    "“The heart keeps getting broken until it stays open” —Thundercat",
    "“If everything you try works, you aren't trying hard enough.” —Gordon Moore",
    "“Nature does not hurry, yet everything is accomplished” —Lao Tzu",
    "“If you can't explain it simply, you don't understand it well enough.” —Albert Einstein",
    "“The chains of habit are too light to be felt until they are too heavy to be broken.”",
    "“When we lose our principles, we invite chaos” —Irving from Mr. Robot",
    "“Even extraordinary people, and I believe you are, are driven by human banalities” —Tyrell Wellick from Mr. Robot",
    "“The world is a dangerous place, Elliott, not because of those who do evil, but because of those who look on and do nothing” —Mr. Robot from Mr. Robot",
    "“Give a man a gun and he can rob a bank, but give a man a bank, and he can rob the world.” —Tyrell Wellick from Mr. Robot",
    "“Fear is like a fire. If you can control it, it can cook for you. It can heat your house.If you can't control it, it will burn everything around you and destroy you. Fear is your friend and your worst enemy” —Sui Ishida",
    "“The most common way people give up their power is by thinking they dont have any” —Alice Walker",
    "“These violent delights have violent ends” —Friar Lawrence from Romeo & Juliet/Westworld",
    "“Running away from a problem only increases the distance from the solution”",
    "“The only thing necessary for the triumph of evil is for good men to do nothing”",
    "“Ihminen on lapsi, hautaan asti” —Aivovuoto. Roughly translated from Finnish to English, “Human being is child till the grave”",
    "“Great spirits have always encountered violent opposition from mediocre minds. The mediocre mind is incapable of understanding the man who refuses to bow blindly to conventional prejudices and chooses instead to express his opinions courageously and honestly” —Albert Einstein",
    "“Use your smile to change the world; don’t let the world change your smile.”",
    "“If we don’t mark the milestones, we’re just passing with the time.” —Lara Axelrod",
    "“Discipline, doing what you hate to do, but nonetheless doing it like you love it.” —Mike Tyson",
    "“You either have 99 problems or a health problem”",
    "“Bloom where you are planted”",
    "“Don't let perfect be the enemy of good”",
    "“Don’t let potential be written on your tombstone”",
    "“My friends don't understand we all are lost” —Mondo Cozmo",
    "“You cannot swim for new horizons until you have courage to lose sight of the shore.” —William Faulkner",
    "“Where you invest your love, you invest your life” —Mumford & Sons",
    "“Achieve more in failure than most do in success”",
    "“Winners focus on winning. Losers focus on winners”",
    "“Aragorn : What do you fear, my lady?\nEowyn : A cage. To stay behind bars until use and old age accept them and all chance of valor has gone beyond recall or desire.” -From The Lord of the Rings: The Two Towers"
]

# Total quotes:
# print(len(quotes))


def send_email(Name, email_receiver):
    em = EmailMessage()
    em['From'] = formataddr(("Daily QOTD", f"{email_sender}"))
    em['To'] = email_receiver

    # gives somebody a default name randomly
    defaultName = ["King", "Monkey", "Buns", "Queen", "Nooblet", "Panda", "Smooshie", "Duckie", "Luigi", "Cheeky",
                   "Captain America", "Gandalf", "Flippers", "Butters", "Doofus", "Bambi", "Cinnamon", "Silly", "Billy", "Tarzan", "Kitty", "Pipsqueak",
                   "Mario", "Pikachu", "Sonic the Hedgehog", "Link", "Master Chief", "Donkey Kong", "Crash Bandicoot", "Zelda"]

    if (Name == None):
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
