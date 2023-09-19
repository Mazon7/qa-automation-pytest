from constants import QA_EMAIL, QA_PASSWORD
class AuthUser:
    data = {"login": QA_EMAIL, "password": QA_PASSWORD}

    @staticmethod
    def get_body(user, pass_w):
        email = user
        password = pass_w
        print(email, password)
        return {"login": email, "password": password}


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
