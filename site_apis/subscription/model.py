from constants import CARD_USER_ID, QA_EMAIL, CARD_ID, CARD_NUMBER, CARD_CRYPTOPROGRAM_PACKET
class SubscriptionData:
    card_data = {"user_id": CARD_USER_ID,
                 "name": "TEST_USER",
                 "exp_date_month": "04",
                 "exp_date_year": "24",
                 "card_number": CARD_NUMBER,
                 "country_code_iso": "RU",
                 "is_default": True,
                 "card_cryptogram_packet": "string"
                 }

    card_upd_data = {"is_default": False}

    sun_renewal_data = {
        "card_id": CARD_ID,
        "email": QA_EMAIL
    }

    # TEST DATA FOR CLOUDPAYMENTS DEV ENV
    cloudpayments_dev = {
        "service": "CLOUDPAYMENTS",
        "card_cryptogram_packet": CARD_CRYPTOPROGRAM_PACKET,
        "email": QA_EMAIL,
        "cvv": "111",
        "name": "crocodile",
        "card_number": CARD_NUMBER,
        "exp_date_month": "01",
        "exp_date_year": "25",
        "save_card": False,
        "country_code_iso": "RU",
        "is_default": False
    }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
