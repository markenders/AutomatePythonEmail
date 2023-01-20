from datetime import date
from Sendemail import send_email
import gspread

# open google account and sheet title/worksheet
sa = gspread.service_account()
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
