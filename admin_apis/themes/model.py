import random
import string

# Get random name
letters = string.ascii_letters
theme_name = 'RandomTheme_' + \
    "".join(random.choice(letters) for i in range(10))


class AdminThemesData:
    def __init__(self, subject_id):
        self.data = {
            "title": theme_name,
            "descriptions": "Test Theme QA",
            "is_active": True,
            "subject_id": subject_id,
            "position": 1
        }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
