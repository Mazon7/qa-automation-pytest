from site_apis.auth.api import Auth
from site_apis.auth.model import AuthUser
from site_apis.schemas.auth import valid_schema

from site_apis.user.api import User
from site_apis.user.model import UserData

from site_apis.subject.api import Subject
from site_apis.subject.model import SubjectData

from site_apis.themes.api import Themes
from site_apis.themes.model import ThemesData

from site_apis.subscription.api import Subscription
from site_apis.subscription.model import SubscriptionData

from site_apis.settings.api import Settings
from site_apis.settings.model import SettingsData

from site_apis.file.api import File
from site_apis.file.model import FileData

from admin_apis.subject.model import AdminSubjectData

from conftest import UIDValueStorage, CardValueStorage, FileValueStorage, ConfirmationValueStorage


import allure
import pytest
from collections.abc import Iterable
import time
import random
import string
from pytest_steps import test_steps

from constants import API_QA_URL, API_DEV_URL, SITE_HEADER, QA_AUTOTEST_EMAIL, QA_EMAIL, QA_PASSWORD, ADMIN_USER_ID


# Helper functions/data
accept = {"Accept": SITE_HEADER}


def get_tokens(url=API_QA_URL, user=QA_AUTOTEST_EMAIL, password=QA_PASSWORD):
    body = AuthUser.get_body(user, password)
    response = Auth(url=url).get_tokens(
        body=body, headers=accept, schema=valid_schema)
    return response.response


@allure.story('User API')
class TestUser:
    @allure.title('Register user')
    @pytest.mark.register_user
    def test_register_user_email(self):
        response = User(url=API_QA_URL).user_register_email(
            body=UserData.random(), headers=accept, schema=valid_schema)
        assert response.status == 201

        time.sleep(5)

    @allure.title('Resend activation')
    @pytest.mark.skip(reason="Bug reported")
    @pytest.mark.resend_activation_email
    def test_resend_activation_email(self):
        response = User(url=API_QA_URL).resend_activation_email(
            body={"email":  UserData.random()["login"]}, headers=accept, schema=valid_schema)
        assert response.status == 204

        time.sleep(5)

    @allure.title('Check code activation and confirm email')
    @pytest.mark.user_activation_email
    def test_user_activation_email(self):
        response = User(url=API_QA_URL).user_activation_email(
            body=UserData.get_activation_data(), headers=accept, schema=valid_schema)
        assert response.status == 204

    @allure.title('Validate and set password')
    # ONLY IF USER AUTHORIZED VIA SOCIAL NETWORKS
    @pytest.mark.skip(reason="USED ONLY IF USER AUTHORIZED VIA SOCIAL NETWORKS google/aplle/vk/telegram")
    @pytest.mark.add_password
    def test_add_password(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        #
        response = User(url=API_QA_URL).add_password(body={"new_password": "87654321"}, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        # resp = response.response
        assert response.status == 200

    @allure.title('Reset password if you forgot it')
    @pytest.mark.reset_password
    def test_reset_password(self):
        token_resp = get_tokens(user=UserData.random(
        )["login"], password=UserData.random()["password"])
        access_token = token_resp["data"]["access"]
        response = User(url=API_QA_URL).reset_password(
            body={"email": UserData.random()["login"]}, headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 204

        time.sleep(5)

    @allure.title('Reset password confirm')
    @pytest.mark.reset_password_confirm
    def test_reset_password_confirm(self):
        token_resp = get_tokens(user=UserData.random(
        )["login"], password=UserData.random()["password"])
        access_token = token_resp["data"]["access"]
        response = User(url=API_QA_URL).reset_password_confirm(body=UserData.get_reset_password_data(
        ), headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 205

    @allure.title('Change password by the user in the personal account')
    @pytest.mark.set_password
    def test_set_password(self):
        token_resp = get_tokens(user=UserData.random(
        )["login"], password="String_12345678")
        access_token = token_resp["data"]["access"]
        response = User(url=API_QA_URL).set_password(body={"new_password": UserData.random()["password"], "current_password": "String_12345678"}, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 205

    @allure.title('Get User Info')
    @pytest.mark.get_user_info
    def test_get_user_info(self):
        token_resp = get_tokens(user=UserData.random(
        )["login"], password=UserData.random()["password"])
        access_token = token_resp["data"]["access"]
        response = User(url=API_QA_URL).get_user_info(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert resp.get("username")

    @allure.title('Update User Info')
    @pytest.mark.update_user_info
    def test_update_user_info(self):
        token_resp = get_tokens(user=UserData.random(
        )["login"], password=UserData.random()["password"])
        access_token = token_resp["data"]["access"]
        #
        response = User(url=API_QA_URL).update_user_info(body=UserData.user_data, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        # CHECK ASSEETIONS
        # assert resp.get("username") == UserData.user_data["username"]
        # assert resp.get("first_name") == UserData.user_data["first_name"]
        # assert resp.get("last_name") == UserData.user_data["last_name"]
        # assert resp.get("middle_name") == UserData.user_data["middle_name"]
        # assert resp.get("email") == UserData.user_data["email"]
        # assert resp.get(
        #     "is_email_confirmed") == UserData.user_data["is_email_confirmed"]
        # assert resp.get(
        #     "email_recovery") == UserData.user_data["email_recovery"]
        # assert resp.get(
        #     "phone_number_primary") == UserData.user_data["phone_number_primary"]
        # assert resp.get(
        #     "is_phone_number_primary_confirmed") == UserData.user_data["is_phone_number_primary_confirmed"]
        # assert resp.get("gender") == UserData.user_data["gender"]
        # assert resp.get("birthdate") == UserData.user_data["birthdate"]
        # assert resp.get(
        #     "avatar_image_id") == UserData.user_data["avatar_image_id"]

    @allure.title('Part Update User Info')
    @pytest.mark.part_upd_user_info
    def test_part_upd_user_info(self):
        token_resp = get_tokens(user=UserData.random(
        )["login"], password=UserData.random()["password"])
        access_token = token_resp["data"]["access"]
        #
        response = User(url=API_QA_URL).part_upd_user_info(body=UserData.part_upd_user, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert resp.get("gender") == UserData.part_upd_user["gender"]
        assert resp.get("birthdate") == UserData.part_upd_user["birthdate"]

    @allure.title('Delete User')
    @pytest.mark.skip(reason="USER DELETE ROUTE IS NOT USED")
    @pytest.mark.delete_user
    def test_delete_user(self):
        token_resp = get_tokens(user=UserData.random()[
                                "login"], password=UserData.random()["password"])
        access_token = token_resp["data"]["access"]
        #
        response = User(url=API_QA_URL).delete_user(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 204


@allure.feature('Auth')
@allure.story('Auth API')
class TestAuth:
    @allure.title('Get access/refresh token')
    def test_get_tokens(self):
        # If there are access & refresh tokens recieved
        # We assume that response code is 200
        token_resp = get_tokens()
        response = token_resp["data"]
        assert response.get('access')
        assert response.get('refresh')

    @pytest.mark.check_token
    def test_check_token(self):
        token_resp = get_tokens()
        tokens = token_resp["data"]
        response1 = Auth(url=API_QA_URL).check_token(
            body={"token": tokens["access"]}, headers=accept, schema=valid_schema)
        response2 = Auth(url=API_QA_URL).check_token(
            body={"token": tokens["refresh"]}, headers=accept, schema=valid_schema)
        assert response1.status == 200
        assert response2.status == 200

    @pytest.mark.get_auth_code
    def test_get_auth_code(self):
        response = Auth(url=API_QA_URL).get_auth_code(body={
            "email": QA_AUTOTEST_EMAIL}, headers=accept, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert resp.get('data')['uid']
        #
        UIDValueStorage.id = resp.get('data')['uid']
        time.sleep(3)

    @pytest.mark.login_with_code
    def test_login_with_code(self):
        # GET AUTH CODE FROM EMAIL BOX
        response = Auth(url=API_QA_URL).login_with_code(body={
            "uid": UIDValueStorage.id, "authorization_code": UserData.get_auth_code()}, headers=accept, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        # assert resp.get('data')
        # ADD ASSERTIONS IF NEEDED
        # CHECK ADDITIONALLY IF USER IS VERIFIED

    def test_logout(self):
        token_resp = get_tokens()
        response = Auth(url=API_QA_URL).log_out(
            body={"refresh_token": token_resp["data"]["refresh"]}, headers=accept, schema=valid_schema)
        assert response.status == 205

    def test_refresh(self):
        # user=UserData.random()["login"], password="87654321"
        token_resp = get_tokens()
        response = Auth(url=API_QA_URL).refresh_token(body={
            "refresh": token_resp["data"]["refresh"]}, headers=accept, schema=valid_schema)
        assert response.status == 200

    @pytest.mark.skip()
    def test_apple_auth(self):
        token_resp = get_tokens()

        response = Auth(url=API_QA_URL).apple_auth(body={
            "access_token": token_resp["data"]["access"],
            "code": "string",
            "id_token": "string"
        }, headers=accept, schema=valid_schema)
        assert response.status == 200

    @pytest.mark.skip()
    def test_google_auth(self):
        token_resp = get_tokens()

        response = Auth(url=API_QA_URL).google_auth(body={
            "access_token": token_resp["data"]["access"],
            "code": "string",
            "id_token": "string"
        }, headers=accept, schema=valid_schema)
        assert response.status == 200

    @pytest.mark.skip(reason="WAIT FOR FIX")
    def test_telegram_auth(self):
        token_resp = get_tokens()

        response = Auth(url=API_QA_URL).telegram_auth(body={
            "access_token": token_resp["data"]["access"],
            "code": "string",
            "id_token": "string"
        }, headers=accept, schema=valid_schema)
        assert response.status == 200

    @pytest.mark.skip(reason="WAIT FOR FIX")
    def test_vk_auth(self):
        token_resp = get_tokens()

        response = Auth(url=API_QA_URL).vk_auth(body={
            "access_token": token_resp["data"]["access"],
            "code": "string",
            "id_token": "string"
        }, headers=accept, schema=valid_schema)
        assert response.status == 200

    @pytest.mark.skip(reason="2FA ROUTE IS NOT USED!")
    def test_two_fa(self):
        token_resp = get_tokens()
        response = Auth(url=API_QA_URL).two_fa(body={
            "login": QA_AUTOTEST_EMAIL,
            "password": QA_PASSWORD
        }, headers=accept, schema=valid_schema)
        assert response.status == 201


@allure.story('Subject')
class TestSubject:
    @allure.title('Subject')
    @pytest.mark.get_subjects
    def test_get_subjects(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subject(url=API_QA_URL).get_subjects(
            headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200

    @pytest.mark.get_subject_id
    def test_get_subject_id(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subject(url=API_QA_URL).get_subject_id(id="BFBRXDSE", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        # BFBRXDSE
        resp = response.response
        assert response.status == 200

    @pytest.mark.subjects_available
    # USER MUST BE GENERAL USER AND SOME COURSES SHOULD BE AVAILABLE FOR BUYING
    # @pytest.mark.skip(reason="data is empty!")
    # GET 500 error if Authorization is specified!
    def test_subjects_available(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]

        response = Subject(url=API_QA_URL).subjects_available(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        data = resp.get("data")
        assert data["id"]
        assert data["title"]
        assert data["descriptions"]
        assert data["logo"]
        assert data["is_active"]
        assert data["tariffs"]
        assert data["access_type"]
        assert data["trial_period_days"] == None
        assert data["trial_left"] == None
        assert data["descriptions_link"]
        assert data["is_shadow"] == False

    @pytest.mark.my_subjects
    def test_my_subjects(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]

        response = Subject(url=API_QA_URL).my_subjects(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200

    @pytest.mark.sub_subjects_id
    # GET SUBSCRIPTION ID FROM users/me route
    @pytest.mark.skip(reason="ROUTE IS NOT USED ON THE FRONTEND!")
    def test_sub_subjects_id(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]

        response = Subject(url=API_QA_URL).sub_subjects_id(id="135e3132-cffe-4bb6-adef-7efe06b884a1",
                                                    headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200

    @pytest.mark.get_current_job
    # @pytest.mark.skip(reason="WAIT FOR SUBSCRIBED COURSE ID")
    def test_get_current_job(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]

        response = Subject(url=API_QA_URL).get_current_job(subject_pk="FCGFDC5S", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200


@allure.story('Themes, Education Script, Video Lesson, Excersice, Conspectus, Bot Script, Text Lesson')
class TestThemes:
    @allure.title('Get All Themes')
    @pytest.mark.get_all_themes
    def test_get_all_themes(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_all_themes(subject_pk="FCGFDC5S", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert isinstance(resp.get("data"), Iterable)

    @allure.title('Get Theme by id')
    @pytest.mark.get_theme
    def test_get_theme(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_theme(id="Q4VBYD2D", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("created_at")
        assert resp.get("modified_at")
        assert resp.get("title")
        assert resp.get("descriptions")
        assert resp.get("position")
        assert resp.get("logo") == None
        assert resp.get("is_active")
        assert resp.get("subject")
        assert isinstance(resp.get("video_lessons"), Iterable)
        assert isinstance(resp.get("video_stubs"), Iterable)
        assert isinstance(resp.get("exercises"), Iterable)
        assert isinstance(resp.get("education_script"), Iterable)

    @allure.title('Complete all points in education script')
    @pytest.mark.complete_education_script
    def test_complete_education_script(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).complete_education_script(id="4f3e8749-d29f-459d-bcb9-784adc31e3ed", headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 200

    @allure.title('Get education script')
    @pytest.mark.get_education_script
    def test_get_education_script(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_education_script(id="Q4VBYD2D", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("created_at")
        assert resp.get("created_at")
        assert resp.get("title")
        assert isinstance(resp.get("points"), Iterable)
        assert resp.get("is_active")

    @allure.title('Get all video lessons')
    @pytest.mark.skip("This Route is not found in docs --> /api/themes//{id/}/video_lessons. Get 404 error!")
    @pytest.mark.get_all_video_lessons
    def test_get_all_video_lessons(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_all_video_lessons(theme_pk="Q4VBYD2D", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert isinstance(resp.get("data"), Iterable)

    @allure.title('Get video by id')
    @pytest.mark.get_video_lesson
    def test_get_video_lesson(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        # Only moderator can check all video lessons by ID
        response = Themes(url=API_QA_URL).get_video_lesson(id="NEE72YIJ", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("created_at")
        assert resp.get("modified_at")
        assert resp.get("job_type")
        assert resp.get("title")
        assert resp.get("description")
        assert resp.get("video_url")
        assert resp.get("is_active")
        assert resp.get("position")
        assert resp.get("lesson_type")
        assert resp.get("duration") == 0
        assert isinstance(resp.get("knowledge"), Iterable)
        assert isinstance(resp.get("attachments"), Iterable)
        assert isinstance(resp.get("theses"), Iterable)

    @allure.title('Get Exercise by id')
    @pytest.mark.get_exercise
    def test_get_exercise(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_exercise(id="395YNI3X", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("question")
        assert resp.get("answer_type")
        assert resp.get("title")
        assert resp.get("description") == ""
        assert resp.get("duration") == 30
        assert resp.get("job_type")
        assert resp.get("answer_options") == None
        assert resp.get("exercise_type")
        isinstance(resp.get("properties"), object)
        assert resp.get("image") == None
        assert resp.get("video_url") == None
        assert resp.get("answer_description")

    @allure.title('Get all exercises')
    @pytest.mark.skip("This Route is not found in docs --> /api/themes//{id/}/exercises. Get 404 error!")
    @pytest.mark.get_all_exercises
    def test_get_all_xercises(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_all_exercises(themes_pk="29T59LP4", headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert isinstance(resp.get("data"), Iterable)

    @allure.title("Check question's answer")
    @pytest.mark.check_answer
    def test_check_answer(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).check_answer(id="EHCGERKX", body=ThemesData.answer_data, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200

    @allure.title("Time is up for exercise")
    @pytest.mark.time_is_up
    def test_time_is_up(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).time_is_up(id="EHCGERKX", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 200

    @allure.title("Get all conspectus")
    @pytest.mark.skip("This Route is not found in docs --> /api/themes//{id/}/conspectus. Get 404 error!")
    @pytest.mark.get_all_conspectus
    def test_get_all_conspectus(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_all_conspectus(id="BFBRXDSE", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200

    @allure.title("Get conspectus by id")
    @pytest.mark.skip(reason="404 Error Not Found?! --> THEME_ID: 29T59LP4, CONSPECTUSS_ID: ABCDBMQF")
    @pytest.mark.get_conspectus
    def test_get_conspectus(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_conspectus(theme_id="29T59LP4", pk_conspectus="ABCDBMQF", page=1, headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200

    @allure.title("Get Bot Script Main Page")
    @pytest.mark.bot_scripts_main
    def test_bot_scripts_main(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).bot_scripts_main(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("created_at")
        assert resp.get("modified_at")
        assert resp.get("title")
        assert isinstance(resp.get("conversations"), Iterable)

    @allure.title("Get Bot Script by id")
    @pytest.mark.get_bot_script
    def test_get_bot_script(self):
        token_resp = get_tokens(user=QA_EMAIL)
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_bot_script(id="C8SHTQ7Z", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        # ADD ASSERTIONS

    @allure.title("Get Text Lesson by id")
    @pytest.mark.get_text_lesson
    def test_get_text_lesson(self):
        token_resp = get_tokens(user=QA_EMAIL)
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_text_lesson(id="HEG0AWK4", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("created_at")
        assert resp.get("modified_at")
        assert resp.get("title")
        assert resp.get("theme")
        assert resp.get("text")
        assert resp.get("is_active")
        assert resp.get("language")
        assert resp.get("files")

    @allure.title("Get all Text Lessons")
    @pytest.mark.skip("This Route is not found in docs --> /api/themes//{id/}/text_lessons. Get 404 error!")
    @pytest.mark.get_all_lessons
    def test_get_all_lessons(self):
        token_resp = get_tokens(user=QA_EMAIL)
        access_token = token_resp["data"]["access"]
        response = Themes(url=API_QA_URL).get_all_lessons(theme_id="4GA7LI0F", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert isinstance(resp, Iterable)


@allure.story('Payments and Subscribes')
class TestSubscription:
    @allure.title('Add card')
    @pytest.mark.add_card
    def test_add_card(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).add_card(body=SubscriptionData.card_data, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 201
        #
        CardValueStorage.id = resp.get("id")
        assert resp.get("name") == SubscriptionData.card_data["name"]
        assert resp.get(
            "exp_date_month") == SubscriptionData.card_data["exp_date_month"]
        assert resp.get(
            "exp_date_year") == SubscriptionData.card_data["exp_date_year"]
        assert resp.get(
            "is_default") == SubscriptionData.card_data["is_default"]
        assert resp.get(
            "country_code_iso") == SubscriptionData.card_data["country_code_iso"]

    @allure.title('Update card')
    @pytest.mark.update_card
    def test_update_card(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).update_card(id=CardValueStorage.id, body=SubscriptionData.card_upd_data, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get(
            "is_default") == SubscriptionData.card_upd_data["is_default"]

    @allure.title('Get cards')
    @pytest.mark.get_cards
    def test_get_cards(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).get_cards(
            headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert isinstance(resp, Iterable)

    @allure.title('Delete card')
    @pytest.mark.delete_card
    def test_delete_card(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).delete_card(id=CardValueStorage.id, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 204

    @allure.title('Get payment history')
    # ADD PAYMENTS DATA FOR USER
    @pytest.mark.get_payment_history
    def test_get_payment_history(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).get_payment_history(
            headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert isinstance(resp, Iterable)

    @allure.title('Subscribe a free subject')
    @pytest.mark.sub_free_subject
    def test_sub_free_subject(self, get_free_subject_id, delete_free_subject_after):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).sub_free_subject(id=get_free_subject_id, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 201

    @allure.title('Subscribe a trial subject')
    @pytest.mark.sub_trial_subject
    def test_sub_trial_subject(self, get_trial_subject_id, delete_trial_subject_after):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).sub_trial_subject(id=get_trial_subject_id, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 201

    @allure.title('Subscribe to a paid subject (Cloudpayments). Tested on DEV env.')
    @pytest.mark.subscribe_with_cloudpayments
    @pytest.mark.skip(reason="CAN BE TESTED ONLY ON DEV")
    def test_subscribe_with_cloudpayments(self):
        token_resp = get_tokens(
            API_DEV_URL, QA_EMAIL, QA_PASSWORD)
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_DEV_URL).subscribe_with_cloudpayments(id="JEJE1TFN", body=SubscriptionData.cloudpayments_dev, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 201
        assert resp.get("modified_at")
        assert resp.get("title")
        assert resp.get("theme")
        assert resp.get("text")
        ConfirmationValueStorage.id = resp.get("id")
        ConfirmationValueStorage.MD = resp.get("MD")
        ConfirmationValueStorage.PaReq = resp.get("PaReq")
        ConfirmationValueStorage.service = resp.get("service")
        ConfirmationValueStorage.subject_id = resp.get("subject")["id"]
        ConfirmationValueStorage.tariff_id = resp.get("tariff_id")
        ConfirmationValueStorage.status = resp.get("status")

    @allure.title('Payment confirmation PULPAL/UseGateway')
    # Для PULPAL необходимо заполнить поля: [service, external_id, status]
    # Для UseGateway необходимо заполнить поля: [service, user_id, subject_id, tariff_id]
    @pytest.mark.skip(reason="NEED TO CHECK!")
    @pytest.mark.payment_confirmation
    def test_payment_confirmation(self):
        token_resp = get_tokens(
            API_DEV_URL, QA_EMAIL, QA_PASSWORD)
        access_token = token_resp["data"]["access"]

        data = {
            "service": ConfirmationValueStorage.service,
            "user_id": ADMIN_USER_ID,
            "subject_id": ConfirmationValueStorage.subject_id,
            "external_id": ConfirmationValueStorage.id,
            "status": ConfirmationValueStorage.status,
            "tariff_id": ConfirmationValueStorage.tariff_id,
        }
        response = Subscription(url=API_DEV_URL).payment_confirmation(body=data, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 200

    @allure.title('Payment confiramtion with 3ds-cards (Cloudpayments). Tested on DEV env.')
    @pytest.mark.payment_confirm_3ds
    @pytest.mark.skip(reason="500 error! NEED TO CHECK!")
    def test_payment_confirm_3ds(self):
        token_resp = get_tokens(
            API_DEV_URL, QA_PASSWORD, QA_PASSWORD)
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_DEV_URL).payment_confirm_3ds(id=ConfirmationValueStorage.id, body={
            "MD": ConfirmationValueStorage.MD, "PaReq": ConfirmationValueStorage.PaReq}, headers={**{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 201
        assert resp.get("modified_at")
        assert resp.get("title")
        assert resp.get("theme")
        assert resp.get("text")

    @allure.title('Unsubscribe from the subject')
    @pytest.mark.unsubscribe_subject
    @pytest.mark.skip(reason="CAN NOT CREATE SUBSCRIPTION via API FOR THIS TEST!")
    # CREATE SUBSCRIPTION FOR SUBJECT WITH PAID TARIF FOR TEST AND PASS ID OF SUBSCRIPTION
    def test_unsubscribe_subject(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).unsubscribe_subject(id="", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 200

    @allure.title('Subject subscription renewal')
    @pytest.mark.skip(reason="CAN NOT CREATE SUBSCRIPTION via API FOR THIS TEST!")
    # PASS SUBSCRIBTION ID FROM THE PREVIOUS TEST
    @pytest.mark.sub_renewal
    def test_sub_renewal(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Subscription(url=API_QA_URL).sub_renewal(id="", body=SubscriptionData.sun_renewal_data, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 201


@ allure.story('Settings')
class TestSettings:
    @ allure.title('Create a Userecho message')
    @ pytest.mark.create_userecho_message
    def test_create_userecho_message(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Settings(url=API_QA_URL).create_userecho_message(data=SettingsData.data, files=SettingsData.files, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 200

    @ allure.title('Get a Userecho categories')
    @ pytest.mark.get_userecho_categories
    def test_get_userecho_categories(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Settings(url=API_QA_URL).get_userecho_categories(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert isinstance(resp, Iterable)

    @ allure.title('Get locale json file')
    @ pytest.mark.get_locale_json
    def test_get_locale_json(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Settings(url=API_QA_URL).get_locale_json(lang="ru", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response
        assert response.status == 200
        assert resp.get("common-back")
        assert resp.get("common")
        assert resp.get("header")
        assert resp.get("nav")

    @ allure.title('Get a site settings')
    @ pytest.mark.get_site_settings
    def test_get_site_settings(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Settings(url=API_QA_URL).get_site_settings(headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200

    @ allure.title('Get a site settings')
    @ pytest.mark.get_site_page
    def test_get_site_page(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = Settings(url=API_QA_URL).get_site_page(slug="mysubjects", headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")
        assert resp.get("slug")
        assert resp.get("name")
        assert resp.get("meta_title")
        assert resp.get("meta_description") == ""
        assert resp.get("meta_keywords") == ""
        assert resp.get("is_animation_enabled") == False
        assert resp.get("is_sidebar_initially_displayed") == False
        assert resp.get("is_sidebar_collapsable") == False
        assert resp.get("is_active")
        assert resp.get("created_at")
        assert resp.get("modified_at")
        assert resp.get("blocks")
        assert resp.get("language_code")


@ allure.story('Test File')
class TestFile:
    @ allure.title('Upload file')
    @ pytest.mark.upload_file
    def test_upload_file(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = File(url=API_QA_URL).upload_file(data=FileData.data, files=FileData.file, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 201
        assert resp.get("title") == FileData.data["title"]
        assert resp.get("file_url")
        assert resp.get("file_name").startswith(FileData.data["file_name"])
        assert resp.get("is_active") == FileData.data["is_active"]
        assert resp.get("file_type") == FileData.data["file_type"]
        assert resp.get("file_size") == None
        assert resp.get("storage")
        assert resp.get("file_url_webp") == None
        #
        FileValueStorage.id = resp.get("id")
        time.sleep(2)

    @ allure.title('Get file')
    @ pytest.mark.get_file
    def test_get_file(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = File(url=API_QA_URL).get_file(id=FileValueStorage.id, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("id")

    @ allure.title('Update file')
    @ pytest.mark.update_file
    def test_update_file(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = File(url=API_QA_URL).update_file(id=FileValueStorage.id, body=FileData.update_file, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("title") == FileData.update_file["title"]
        assert resp.get("is_active") == FileData.update_file["is_active"]
        assert resp.get("storage") == FileData.update_file["storage"]

    @ allure.title('Part update file')
    @ pytest.mark.part_upd_file
    def test_part_upd_file(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = File(url=API_QA_URL).part_upd_file(id=FileValueStorage.id, body=FileData.part_upd_file, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        resp = response.response["data"]
        assert response.status == 200
        assert resp.get("is_active") == FileData.part_upd_file["is_active"]

    @ allure.title('Delete file')
    @ pytest.mark.delete_file
    def test_delete_file(self):
        token_resp = get_tokens()
        access_token = token_resp["data"]["access"]
        response = File(url=API_QA_URL).delete_file(id=FileValueStorage.id, headers={
            **{"Authorization": f"JWT {access_token}"}, **accept}, schema=valid_schema)
        assert response.status == 204