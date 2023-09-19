import logging
from jsonschema import validate

from site_apis.requests import Client
from site_apis.auth.model import ResponseModel

logger = logging.getLogger("api")


class Auth:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    MAIN_AUTH = '/token'
    LOGIN_WITH_CODE = MAIN_AUTH + '/code'  # Login user with code
    GET_AUTH_CODE = MAIN_AUTH + '/email'
    REFRESH_TOKEN = MAIN_AUTH + '/refresh'
    LOGOUT = MAIN_AUTH + '/logout'
    APPLE_OAUTH = MAIN_AUTH + '/social/apple'
    GOOGLE_OAUTH = MAIN_AUTH + '/social/google'
    TELEGRAM_AUTH = MAIN_AUTH + '/social/telegram'
    VK_AUTH = MAIN_AUTH + '/social/vk'
    LOGIN_2FA = MAIN_AUTH + '/twofa'
    VERIFY_TOKEN = MAIN_AUTH + '/verify'

    def get_tokens(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.MAIN_AUTH}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_auth_code(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.GET_AUTH_CODE}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def login_with_code(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.LOGIN_WITH_CODE}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def refresh_token(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.REFRESH_TOKEN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def log_out(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.LOGOUT}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        # THIS API REQUEST DOESN'T HAVE RESPONSE BODY
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def apple_auth(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.APPLE_OAUTH}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def google_auth(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.GOOGLE_OAUTH}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def telegram_auth(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.TELEGRAM_AUTH}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        # THIS API REQUEST DOESN'T HAVE RESPONSE BODY
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def vk_auth(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.VK_AUTH}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def two_fa(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.LOGIN_2FA}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        # THIS API REQUEST DOESN'T HAVE RESPONSE BODY
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def check_token(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.VERIFY_TOKEN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())
