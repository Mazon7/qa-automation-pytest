class ThemesData:
    answer_data = {
        "user_answer": "да",
        "elapsed_time": 0
    }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
