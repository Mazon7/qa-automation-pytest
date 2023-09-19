from constants import QA_EMAIL

class SettingsData:
    data = {"email": QA_EMAIL,
            "type_error": "Technical issues",
            "description": "Test picture",
            }

    files = {'file': open('test_files/test_doc.txt', 'rb')}


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
