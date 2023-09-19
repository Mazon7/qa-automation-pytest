from constants import ADMIN_USER_ID, QA_EMAIL
class AdminSubscriptionData:
    data = {
        "user_id": ADMIN_USER_ID,
        "email": QA_EMAIL,
        "properties": {},
        "is_gift": False,
        "gift_days": 0,
        "subject_id": "DDAFBE12"
    }

    gift_data = {
        "user_id": ADMIN_USER_ID,
        "is_gift": True,
        "gift_days": 30,
        "subject_id": "R1C3FNGO"
        }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
