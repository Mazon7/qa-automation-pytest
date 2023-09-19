import pytest
import time
import random
import string

from constants import *

from site_apis.auth.api import Auth
from site_apis.auth.model import AuthUser
from site_apis.schemas.auth import valid_schema

from site_apis.user.api import User
from site_apis.user.model import UserData


from admin_apis.subject.api import AdminSubject
from admin_apis.subject.model import AdminSubjectData
# from admin_apis.schemas.subject import valid_schema

from admin_apis.themes.api import AdminThemes
from admin_apis.themes.model import AdminThemesData

from admin_apis.text_lessons.api import AdminTextLessons
from admin_apis.text_lessons.model import AdminTextLessonsData

from admin_apis.education_script.api import AdminEduScript
from admin_apis.education_script.model import AdminEduScriptData

from admin_apis.subscription.api import AdminSubscription
from admin_apis.subscription.model import AdminSubscriptionData

from site_apis.subscription.api import Subscription



# Helper functions/data
admin_accept = {"Accept": ADMIN_HEADER}

def pytest_configure(config):
    # register your new marker to avoid warnings
    config.addinivalue_line("markers", "key: specify a test key")


def pytest_addoption(parser):
    # add your new filter option (you can name it whatever you want)
    parser.addoption('--key', action='store')


def pytest_collection_modifyitems(config, items):
    # check if you got an option like --key=test-001
    filter = config.getoption("--key")
    if filter:
        new_items = []
        for item in items:
            mark = item.get_closest_marker("key")
            if mark and mark.args and mark.args[0] == filter:
                # collect all items that have a key marker with that value
                new_items.append(item)
        items[:] = new_items



@pytest.fixture(scope='session')
def cleanup_actions(request):
    # Perform any setup actions here
    yield
    # Perform teardown actions here


@pytest.fixture()
def get_tokens(url=API_QA_URL, user=QA_EMAIL, password=QA_PASSWORD):
    body = AuthUser.get_body(user, password)
    response = Auth(url=url).get_tokens(
        body=body, headers=admin_accept, schema=valid_schema)
    return response.response


@pytest.fixture()
def generate_email():
    result = time.time()
    seconds = str(result).split('.', 1)[0]
    email = QA_AUTOTEST_ALIAS + (str(seconds)) + "@gmail.com"
    return email


@pytest.fixture()
def get_random_string(length=8):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str


@pytest.fixture()
def get_free_subject_id(get_tokens):
    access_token = get_tokens["data"]["access"]
    # CREATE SUBJECT
    # AdminSubjectData.free_data
    subject_response = AdminSubject(url=API_QA_URL).create_subject(body=AdminSubjectData.free_data, headers={
        **{"Authorization": f"JWT {access_token}"}, **admin_accept})
    subject_id = subject_response.response["data"]["id"]  # Get Subject ID
    # CREATE THEME and assign it to Subject
    themes_response = AdminThemes(url=API_QA_URL).create_theme(body=AdminThemesData(
        subject_id).data, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
    theme_id = themes_response.response["data"]["id"]  # Get Theme ID
    # CREATE EXERCISE - TEXT LESSON
    text_lesson_response = AdminTextLessons(url=API_QA_URL).create_text_lesson(body=AdminTextLessonsData(
        theme_id).data, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
    # Get Text_Lesson ID
    text_lesson_id = text_lesson_response.response["data"]["id"]
    # CREATE EDUCATION SCRIPT FOR SUBJECT
    AdminEduScript(url=API_QA_URL).create_edu_script(body=AdminEduScriptData(
        theme_id, text_lesson_id).data, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})

    return subject_response.response["data"]["id"]


@pytest.fixture()
def get_trial_subject_id(get_tokens):
    access_token = get_tokens["data"]["access"]
    # CREATE SUBJECT
    # AdminSubjectData.free_data
    subject_response = AdminSubject(url=API_QA_URL).create_subject(body=AdminSubjectData.trial_data, headers={
        **{"Authorization": f"JWT {access_token}"}, **admin_accept})
    subject_id = subject_response.response["data"]["id"]  # Get Subject ID
    # CREATE THEME and assign it to Subject
    themes_response = AdminThemes(url=API_QA_URL).create_theme(body=AdminThemesData(
        subject_id).data, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
    theme_id = themes_response.response["data"]["id"]  # Get Theme ID
    # CREATE EXERCISE - TEXT LESSON
    text_lesson_response = AdminTextLessons(url=API_QA_URL).create_text_lesson(body=AdminTextLessonsData(
        theme_id).data, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
    # Get Text_Lesson ID
    text_lesson_id = text_lesson_response.response["data"]["id"]
    # CREATE EDUCATION SCRIPT FOR SUBJECT
    AdminEduScript(url=API_QA_URL).create_edu_script(body=AdminEduScriptData(
        theme_id, text_lesson_id).data, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})

    return subject_response.response["data"]["id"]


@pytest.fixture()
def delete_free_subject_after(get_tokens, get_free_subject_id):
    access_token = get_tokens["data"]["access"]

    subject_id = get_free_subject_id
    yield subject_id
    # Code to use the response after the test is done
    if subject_id is not None:
        # Use the response as needed
        print("Subject ID from get_free_subject_id:", subject_id)
        response = AdminSubject(url=API_QA_URL).delete_subject(id=subject_id, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
        assert response.status == 204

@pytest.fixture()
def delete_trial_subject_after(get_tokens, get_trial_subject_id):
    access_token = get_tokens["data"]["access"]

    subject_id = get_trial_subject_id
    yield subject_id
    # Code to use the response after the test is done
    if subject_id is not None:
        # Use the response as needed
        print("Subject ID from get_trial_subject_id:", subject_id)
        response = AdminSubject(url=API_QA_URL).delete_subject(id=subject_id, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
        assert response.status == 204

@pytest.fixture()
def gift_a_subscription(get_tokens):
    access_token = get_tokens["data"]["access"]
    gifted_subscription = AdminSubscription(url=API_QA_URL).create_subscription(subjects_pk="R1C3FNGO", body=AdminSubscriptionData.gift_data, headers={ **{"Authorization": f"JWT {access_token}"}, **admin_accept})
    gifted_subscription_id = gifted_subscription.response['data']['id']
    return gifted_subscription_id

@pytest.fixture()
def delete_subscription_after(request, get_tokens, gift_a_subscription):
    # yield
    # Add a finalizer to the request to call delete_subscription_after after the test
    request.addfinalizer(lambda: delete_subscription_after_func(get_tokens, gift_a_subscription))
    # The fixture itself doesn't return anything

def delete_subscription_after_func(get_tokens, gifted_subscription_id):
    access_token = get_tokens["data"]["access"]
    # REMOVE SUBSCRIPTION using the gifted_subscription_id
    response = AdminSubscription(url=API_QA_URL).delete_subscription(id=gifted_subscription_id, headers={**{"Authorization": f"JWT {access_token}"}, **admin_accept})
    assert response.status == 204


@pytest.fixture()
def delete_subscription(get_tokens):
    yield
    access_token = get_tokens["data"]["access"]
    # GET SUBSCRIPTION ID BY GET /users/me

    subscriptions_resp = AdminSubscription(url=API_QA_URL).get_subscriptions_by_subject(subjects_pk="DPBA7D3V", headers={ **{"Authorization": f"JWT {access_token}"}, **admin_accept})

    subscription_id = None
    for subscription in subscriptions_resp.response['data']:
        if subscription["user"]["email"] == QA_AUTOTEST_EMAIL:
            subscription_id = subscription["id"]
    
    # REMOVE SUBSCRIPTION
    response = AdminSubscription(url=API_QA_URL).delete_subscription(id=subscription_id, headers={
        **{"Authorization": f"JWT {access_token}"}, **admin_accept})
    assert response.status == 204

# @pytest.mark.usefixtures("cleanup_actions")
# @pytest.fixture()
# def pytest_sessionfinish(session, exitstatus, get_tokens):
#     """
#     Called after whole test run finished, right before
#     returning the exit status to the system.
#     """
#     print("All tests have been executed. Running cleanup actions...")
#     # Your code goes here


class UIDValueStorage:
    id = None


class CardValueStorage:
    id = None


class FileValueStorage:
    id = None


class ConfirmationValueStorage:
    MD = None
    PaReq = None
    id = None
    service = None
    subject_id = None
    tariff_id = None
    status = None
