import re
import os.path
import base64
import time
import random
import string

from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import logging
from constants import QA_AUTOTEST_EMAIL, QA_AUTOTEST_ALIAS

logger = logging.getLogger("model")


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str


def generate_email():
    result = time.time()
    seconds = str(result).split('.', 1)[0]
    email = QA_AUTOTEST_ALIAS + (str(seconds)) + "@gmail.com"
    return email


EMAIL = generate_email()
PASSWORD = get_random_string(8)


def get_email_text(email=EMAIL):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        logger.info(creds)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=[
            'INBOX'], q=f"to:{email}", maxResults=1).execute()
        # q="is:unread"
        messages = results.get('messages')

        if not messages:
            print('No new messages.')
        else:
            message_count = 0
            for message in messages:
                # call the function that will call the body of the message
                # get_message(service, message['id'])
                msg = service.users().messages().get(
                    userId='me', id=message["id"], format='full').execute()

                payload = msg['payload']
                headers = payload['headers']
                data = payload['body']['data']
                email_html = base64.urlsafe_b64decode(data).decode()
                soup = BeautifulSoup(email_html)
                text = soup.get_text()
                return text

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


class UserData:
    reserve_codes_data = {
        "code": "1",
        "is_active": True
    }

    user_data = {
        "username": "TestUserName",
        "first_name": "First_Name",
        "last_name": "Last_Name",
        "middle_name": "Middle_Name",
        "email": EMAIL,
        "is_email_confirmed": True,
        "email_recovery": EMAIL,
        "phone_number_primary": "+77777777777",
        "is_phone_number_primary_confirmed": True,
        "gender": "male",
        "birthdate": "2023-05-12",
        # "avatar_image_id": ""
    }

    part_upd_user = {"username": "TestUserNameUpdated",
                     "first_name": "string",
                     "last_name": "string",
                     "middle_name": "string",
                     "email": EMAIL,
                     "is_email_confirmed": True,
                     "phone_number_primary": "string",
                     "is_phone_number_primary_confirmed": True,
                     "gender": "female",
                     "birthdate": "1923-05-12",
                     "avatar_image_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                     "is_terms_of_use_accepted": True
                    }

    @staticmethod
    def get_auth_code():
        message = get_email_text(email=QA_AUTOTEST_EMAIL)
        # REGEX #
        code_regex = r'\d{5}'
        code = re.search(code_regex, message).group()
        logger.info(code)
        return code

    @staticmethod
    def get_activation_link(email):
        message = get_email_text(email)
        logger.info(message)
        link = re.search(
            r'(https?://[^\s]+/activate\?code=[\d&=a-zA-Z]+)', message).group()
        logger.info(link)
        return link

    @staticmethod
    def get_activation_data():
        message = get_email_text()
        # REGEX #
        uid_regex = r'(?<=uid=)[A-Za-z0-9]+'
        code_regex = r'(?<=code=)\d{6}'
        uid = re.search(uid_regex, message).group()
        code = re.search(code_regex, message).group()
        logger.info({"uid": uid, "activation_code": code})
        return {"uid": uid, "activation_code": code}

    @staticmethod
    def get_reset_password_data():
        message = get_email_text()
        # REGEX #
        uid_regex = r'(?<=uid=)[A-Za-z0-9]+'
        code_regex = r'(?<=activation_code=)\d{6}'
        uid = re.search(uid_regex, message).group()
        code = re.search(code_regex, message).group()
        logger.info({"uid": uid, "activation_code": code,
                    "new_password": "String_12345678"})
        return {"uid": uid, "activation_code": code, "new_password": "String_12345678"}

    @staticmethod
    def random():
        email = EMAIL
        password = PASSWORD
        print(email, password)
        return {"login": email, "password": password}


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
