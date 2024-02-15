import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_id_client_secret_2023-05-27.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        deleted_message_count = 0
        f = open("email_id.txt", "r")
        for email_id in f:
            deleted_message_count = deleted_message_count + list_and_delete_messages(
                service, email_id.strip("\n")
            )

        print("Total deleted messages: " + str(deleted_message_count))

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


def list_and_delete_messages(service, emailId):
    total_deleted_messages = 0
    user = "me"
    messages = (
        service.users().messages().list(userId=user, q="from:" + emailId).execute()
    )
    if messages["resultSizeEstimate"] == 0:
        print(emailId + ": No message exist")
    else:
        message_count = len(messages["messages"])
        for message in messages["messages"]:
            message_id = message["id"]
            service.users().messages().trash(userId=user, id=message_id).execute()
            total_deleted_messages = total_deleted_messages + 1
        print(
            emailId
            + ": Deleted "
            + str(message_count)
            + (" messages" if message_count > 1 else " message")
        )
    return total_deleted_messages


if __name__ == "__main__":
    main()
