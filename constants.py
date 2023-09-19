# constants.py

"""This module defines project-level constants."""

from dotenv import load_dotenv
import os

load_dotenv('.env')

# ADMIN API SECTION
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
QA_EMAIL = os.getenv('QA_EMAIL')
QA_PASSWORD = os.getenv('PASSWORD')
ADMIN_HEADER = os.getenv('ADMIN_HEADER')

# SITE SECTION
API_QA_URL = os.getenv('API_QA_URL')
API_DEV_URL = os.getenv('API_DEV_URL')
SITE_QA_URL = os.getenv('SITE_QA_URL')
QA_AUTOTEST_ALIAS = os.getenv('QA_AUTOTEST_ALIAS')
QA_AUTOTEST_EMAIL = os.getenv('QA_AUTOTEST_EMAIL')
SITE_HEADER = os.getenv('SITE_HEADER')
TELEGRAM_BOT_LINK = os.getenv('TELEGRAM_BOT_LINK')
TELEGRAM_LINK = os.getenv('TELEGRAM_LINK')

# CARD DATA
CARD_USER_ID = os.getenv('CARD_USER_ID')
CARD_ID = os.getenv('CARD_ID')
CARD_NUMBER = os.getenv('CARD_NUMBER')
CARD_CRYPTOPROGRAM_PACKET = os.getenv('CARD_CRYPTOPROGRAM_PACKET')