from datetime import date
from Sendemail import send_email
from dotenv import load_dotenv
import gspread
import os

# load env vars
load_dotenv()

# format with .replace
pkey = os.getenv('private_key').replace('\\n', '\n')

credentials = {
    "type": "service_account",
    "project_id": os.getenv('project_id'),
    "private_key_id": os.getenv('private_key_id'),
    "private_key": pkey,
    "client_email": os.getenv('client_email'),
    "client_id": os.getenv('client_id'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('client_x509_cert_url')
}

sa = gspread.service_account_from_dict(credentials)
sh = sa.open("DailyEmailPythonResponses")
wks = sh.worksheet("Sheet1")

print('Emails to be sent: ', wks.row_count-1)

# last row to go to
maxrow = wks.row_count
# first row to start on
row = 2
# tracks emails sent
sentEmails = 0

while row <= maxrow:
    send_email(
        Name=wks.acell('B'+str(row)).value,
        email_receiver=wks.acell('C'+str(row)).value
    )
    row += 1
    sentEmails += 1

print('Total emails sent: ' + str(sentEmails))
