import logging
from jsonschema import validate

from site_apis.requests import Client
from site_apis.themes.model import ResponseModel

logger = logging.getLogger("api")


class Themes:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    MAIN = "/themes"
    EDUCATION_SCRIPT = "/education_script"
    VIDEO_LESSONS = "/video_lessons"
    EXERCISES = "/exercises"
    CONSPECTUS = "/conspectus"
    BOT_SCRIPT = "/bot_scripts"
    TEXT_LESSONS = "/text_lessons"

    def get_all_themes(self, subject_pk: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}/subjects/{subject_pk}{self.MAIN}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_theme(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def complete_education_script(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.EDUCATION_SCRIPT}/{id}/complete", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_education_script(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{id}{self.EDUCATION_SCRIPT}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_all_video_lessons(self, theme_pk: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{theme_pk}{self.VIDEO_LESSONS}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_video_lesson(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.VIDEO_LESSONS}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_exercise(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.EXERCISES}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_all_exercises(self, themes_pk: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{themes_pk}{self.EXERCISES}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def check_answer(self, id: str, body: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.EXERCISES}/{id}/checking", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def time_is_up(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.EXERCISES}/{id}/time_is_up", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_all_conspectus(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{id}{self.CONSPECTUS}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_conspectus(self, theme_id: str, pk_conspectus: str, page: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{theme_id}{self.CONSPECTUS}/{pk_conspectus}/{page}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def bot_scripts_main(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}/bot_script_main_page", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_bot_script(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.BOT_SCRIPT}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_text_lesson(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.TEXT_LESSONS}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_all_lessons(self, theme_id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{theme_id}{self.TEXT_LESSONS}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())
