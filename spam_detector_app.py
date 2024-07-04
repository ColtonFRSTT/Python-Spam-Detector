# @ Colton .S.T.T Fridgen

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from spam_detector import predict

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"]

def detect_spam():
  """
  Detects spam emails in the user's Gmail inbox.

  This function authenticates the user, retrieves unread messages from the inbox,
  and checks if each message is spam or not. If a message is identified as spam,
  it is moved to the spam folder.

  Args:
    None

  Returns:
    None
  """
  creds = None

  # Check if token file exists and load credentials
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  # If credentials are not valid, refresh them
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    # Save the refreshed credentials to token file
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  # Build Gmail service using the credentials
  service = build("gmail", "v1", credentials=creds)

  # Retrieve unread messages from the inbox
  results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
  messages = results.get("messages", [])

  message_count = 0
  # Process each message
  for message in messages:
    msg = service.users().messages().get(userId="me", id=message["id"]).execute()
    message_count += 1
    email_data = msg["payload"]["headers"]
    for values in email_data:
      name = values["name"]
      if name == "From":
        from_name = values["value"]
        print(f"{message_count})")
        print(f"From: {from_name}")
        subject = [j["value"] for j in email_data if j["name"] == "Subject"]
        print(f"Subject: {subject}")

    # Check if the message has text/plain part
    if 'parts' in msg["payload"]:
      for p in msg["payload"]["parts"]:
        if p["mimeType"] == "text/plain":
          data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
          print(f"Body: {data}")

          # Check if the message is spam or not
          if predict(data) == "not spam":
            print("This email is not spam!")
          else:
            print("This email is spam... moving to spam folder!")
            # Move the message to spam folder
            service.users().messages().modify(
              userId="me",
              id=message["id"],
              body={"removeLabelIds": ["INBOX"], "addLabelIds": ["SPAM"]},
            ).execute()
          print()

if __name__ == "__main__":
  detect_spam()