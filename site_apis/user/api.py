import logging
from jsonschema import validate

from site_apis.requests import Client
from site_apis.user.model import ResponseModel

logger = logging.getLogger("api")


class User:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    MAIN_AUTH = '/users'
    RESERVE_CODES = "/user_reserve_codes"
    USER_SESSIONS = "/user_sessions"
    ACTIVATE_EMAIL = MAIN_AUTH + "/activation_email"
    ACTIVATE_PHONE = MAIN_AUTH + "/activation_phone"
    ADD_PASS = MAIN_AUTH + "/add_password"
    USER_MAIN = MAIN_AUTH + "/me"
    RESEND_ACTIVATION = MAIN_AUTH + '/resend_activation'
    RESET_PASS = MAIN_AUTH + '/reset_password'
    RESET_PASS_CONF = MAIN_AUTH + '/reset_password_confirm'
    SET_PASS = MAIN_AUTH + '/set_password'
    USERS_EMAIL = "/users_email"
    USERS_PHONE = "/users_phone"

    def get_reserve_codes(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.RESERVE_CODES}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def create_reserve_codes(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.RESERVE_CODES}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_user_sessions(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.USER_SESSIONS}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def close_user_sessions(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.USER_SESSIONS}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def close_user_session(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "PATCH", f"{self.url}{self.USER_SESSIONS}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def user_activation_email(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.ACTIVATE_EMAIL}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def user_register_email(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.USERS_EMAIL}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def resend_activation_email(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.RESEND_ACTIVATION}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def add_password(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.RESEND_ACTIVATION}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def set_password(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.SET_PASS}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def reset_password(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.RESET_PASS}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def reset_password_confirm(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.RESET_PASS_CONF}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_user_info(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.USER_MAIN}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def update_user_info(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "PUT", f"{self.url}{self.USER_MAIN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def part_upd_user_info(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "PATCH", f"{self.url}{self.USER_MAIN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def delete_user(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "DELETE", f"{self.url}{self.USER_MAIN}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)
