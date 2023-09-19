import random
import string

# Get random name
letters = string.ascii_letters
name = 'EduScript_' + "".join(random.choice(letters) for i in range(10))


class AdminEduScriptData:
    def __init__(self, theme_id, text_lessson_id):
        self.data = {
            "theme_id": theme_id,
            "title": name,
            "is_active": True,
            "points": [
                {
                    "job_object_id": text_lessson_id,
                    "job_type": "text_lesson",  # video_lesson, exercise, bot, text_lesson
                    "position": 1,
                    "is_active": True
                }
            ]
        }


class ResponseModel:
    def __init__(self, status: int, response: dict = None):
        self.status = status
        self.response = response
