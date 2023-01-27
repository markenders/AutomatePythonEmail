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

# open account with creds
sa = gspread.service_account_from_dict(credentials)

# open unsubscribe sheet
unsub = sa.open("UnsubscribeQOTD")
unsubWorksheet = unsub.worksheet("UnsubResponse")

# open subscribe sheet
sh = sa.open("DailyEmailPythonResponses")
wks = sh.worksheet("Sheet1")


# list of emails to be deleted
u_list = unsubWorksheet.col_values(2)

UnsubRow = 1

while (UnsubRow < len(u_list)):
    # list of cell info and email
    unsubtest = (wks.findall(u_list[UnsubRow]))

    # convert from cell to str list
    emailStr = [str(x) for x in unsubtest]
    test = 0

    while (test < len(emailStr)):
        end = emailStr[test].find("C", 7)
        emailStr[test] = str(emailStr[test])[7:end]
        test += 1

    goo = 0
    rowToDel = len(emailStr) - 1

    while (goo < len(emailStr)):
        # Have to go backwards on delete, messes with google sheets otherwise
        wks.delete_rows(int(emailStr[rowToDel]))
        rowToDel -= 1
        goo += 1

    UnsubRow += 1

# reset sheet to two rows
if (len(u_list) >= 3):
    unsubWorksheet.delete_rows(3, len(u_list))

# reset/clear sheet
if (len(u_list) > 1):
    unsubWorksheet.clear()
    unsubWorksheet.update('A1', 'Timestamp')
    unsubWorksheet.update('B1', 'Email_Unsub')
    print('Subscriber sheet updated and Unsubscriber sheet cleared')


# trying to reopen sheet to refresh wasn't updating after unsubscribe fast enough
sh = sa.open("DailyEmailPythonResponses")
wks = sh.worksheet("Sheet1")


# last row to go to
maxrow = wks.row_count
# tracks emails sent
sentEmails = 0
# get email data in list of lists
emailData = wks.get('B2:C'+str(maxrow))


print('Emails to be sent: ', str(len(emailData)))

emailIndex = 0

while emailIndex < len(emailData):
    send_email(
        Name=emailData[emailIndex][0],
        email_receiver=emailData[emailIndex][1]
    )
    emailIndex += 1
    sentEmails += 1

print('Total emails sent: ' + str(sentEmails))
