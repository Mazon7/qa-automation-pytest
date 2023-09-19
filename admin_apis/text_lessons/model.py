import random
import string

# Get random name
letters = string.ascii_letters
name = 'RandomTextLesson_' + "".join(random.choice(letters) for i in range(10))


class AdminTextLessonsData:
    def __init__(self, theme_id):
        self.data = {
            "title": name,
            "text": "Very random random text",
            "theme_id": theme_id,
            "is_active": True,
            "language": "all",
            "file_ids": []
        }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
