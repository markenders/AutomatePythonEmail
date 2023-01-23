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
if (len(u_list) != 1):
    print("Emails to be deleted: " + str(u_list))

    while (1 < len(u_list)):
        # if 2 == row_count last row that cannot be deleted so null values swapped in.
        if (len(u_list) == 2):
            try:
                email = wks.find(u_list[1])
                wks.delete_rows(email.row)
            except:
                print("Couldn't find email in subscriber sheet")
            unsubWorksheet.clear()
            unsubWorksheet.update('A1', 'Timestamp')
            unsubWorksheet.update('B1', 'Email_Unsub')

            # this should break the loop length == 1
            u_list.remove(u_list[1])
        else:
            try:
                email = wks.find(u_list[1])
                wks.delete_rows(email.row)
            except:
                print("couldn't find email")
            unsubWorksheet.delete_rows(2)
            u_list.remove(u_list[1])
    print("Results of unsubscribe (Email_Unsub is supposed to be there): " + str(u_list))


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
