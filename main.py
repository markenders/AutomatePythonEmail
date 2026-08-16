import os
import time
import gspread
from gspread.exceptions import APIError
from Sendemail import send_email
from datetime import date
from dotenv import load_dotenv

# Load env vars
load_dotenv()

raw_pkey = os.getenv('private_key')
pkey = raw_pkey.replace('\\n', '\n') if raw_pkey else ''

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

def open_sheet_with_retry(sa, title, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            return sa.open(title)
        except APIError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Google API unavailable when opening '{title}'. Retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)

# Initialize client
sa = gspread.service_account_from_dict(credentials)

# 1. Fetch unsubscribed emails
unsub_sheet = open_sheet_with_retry(sa, "UnsubscribeQOTD")
unsub_wks = unsub_sheet.worksheet("UnsubResponse")
# Get col 2 values, excluding header if present
raw_unsub_list = unsub_wks.col_values(2)
unsub_emails = set(email.strip().lower() for email in raw_unsub_list[1:] if email.strip())

# 2. Fetch subscribers
sub_sheet = open_sheet_with_retry(sa, "DailyEmailPythonResponses")
sub_wks = sub_sheet.worksheet("Sheet1")
all_subscribers = sub_wks.get_all_values()

if all_subscribers:
    header = all_subscribers[0]
    sub_rows = all_subscribers[1:]
else:
    header = ['Name', 'Email']
    sub_rows = []

# 3. Filter out unsubscribed users in memory
active_subscribers = []
for row in sub_rows:
    if len(row) >= 3:  # Ensure row has at least A, B, and C
        email = row[2].strip().lower()  # Column C is Email
        if email and email not in unsub_emails:
            active_subscribers.append(row)

# 4. Update subscriber sheet in bulk if any unsubscribes occurred
if unsub_emails and len(sub_rows) != len(active_subscribers):
    sub_wks.clear()
    sub_wks.update(values=[header] + active_subscribers, range_name='A1')
    print("Subscriber sheet updated with removals.")

# 5. Clear unsubscribe sheet in one batch call
if unsub_emails:
    unsub_wks.clear()
    unsub_wks.update(values=[['Timestamp', 'Email_Unsub']], range_name='A1')
    print("Unsubscriber sheet cleared.")

# 6. Send emails to active subscribers
print(f"Emails to be sent: {len(active_subscribers)}")
sent_count = 0

for row in active_subscribers:
    name = row[1]      # Column B is Name
    receiver = row[2]  # Column C is Email
    
    try:
        send_email(Name=name, email_receiver=receiver)
        sent_count += 1
    except Exception as e:
        print(f"Failed to send email to {receiver}: {e}")

print(f"Total emails sent: {sent_count}")