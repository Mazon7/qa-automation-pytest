import logging
from jsonschema import validate

from site_apis.requests import Client
from site_apis.subscription.model import ResponseModel

logger = logging.getLogger("api")


class Subscription:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    CARDS = "/cards"
    SUBJECTS = "/subjects"

    def identify_card(self, body: dict, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}/card/{id}/post3ds", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_cards(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.CARDS}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def add_card(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.CARDS}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def update_card(self, body: dict, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "PATCH", f"{self.url}{self.CARDS}/{id}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def delete_card(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "DELETE", f"{self.url}{self.CARDS}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_payment_history(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}/payment_history", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def sub_free_subject(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.SUBJECTS}/{id}/subscription/free", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def sub_trial_subject(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.SUBJECTS}/{id}/subscription/trial", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def sub_renewal(self, id: str, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}/subscribe/renewal/{id}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def unsubscribe_subject(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}/unsubscribe/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def payment_confirmation(self, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}/subscriptions/payment/confirmation", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def payment_confirm_3ds(self, id: str, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}/subscriptions/{id}/post3ds", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def subscribe_with_cloudpayments(self, body: dict, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.SUBJECTS}/tariff/{id}/subscription/paid", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def subscribe_with_usegateway(self, body: dict, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.SUBJECTS}/tariff/{id}/subscription/paid/crypto", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def subscribe_with_pulpal(self, body: dict, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.SUBJECTS}/tariff/{id}/subscription/paid/pulpal", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())
