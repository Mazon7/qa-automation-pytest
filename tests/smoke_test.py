import allure
import pytest
import time
from datetime import date, timedelta
from pytest_steps import test_steps
from seleniumbase import BaseCase
# from selenium_stealth import stealth

from constants import *
from site_apis.user.model import *


class RegisterForm:
    def signup_to_app(self, sb, url, login, password):
        sb.open(url)
        sb.click('button:contains("Регистрация")')
        sb.wait_for_element('input[name="login"]')
        sb.wait_for_element('input[name="password"]')
        sb.click('input[name="login"]')
        sb.type('input[name="login"]', login)
        sb.click('input[name="password"]')
        sb.type('input[name="password"]', password)
        sb.click('input[type="checkbox"] + span')
        sb.click('button[type="submit"]')


class LoginForm:
    def signin_to_app(self, sb, url, login, password):
        sb.open(url)
        sb.click('button:contains("Вход")')
        sb.click('span:contains("Войти с помощью пароля")')
        sb.wait_for_element('input[name="login"]')
        sb.wait_for_element('input[name="password"]')
        sb.click('input[name="login"]')
        sb.type('input[name="login"]', login)
        sb.click('input[name="password"]')
        sb.type('input[name="password"]', password)
        sb.click('button[type="submit"]')


@allure.story('SignUp')
class SignUpTests(BaseCase):
    @pytest.mark.sign_up
    def test_signup_to_app(self):
        RegisterForm().signup_to_app(self, SITE_QA_URL, generate_email(), get_random_string(8))
        self.assert_element('div#modal')

    @pytest.mark.confirm_sign_up
    def test_signup_confirm(self):
        email = generate_email()
        password = get_random_string(8)
        RegisterForm().signup_to_app(self, SITE_QA_URL, email, password)
        # check email and confirm registration
        time.sleep(5)
        link = UserData.get_activation_link(email)
        time.sleep(2)
        self.open(link)
        self.wait_for_element('div:contains("Ваш адрес успешно активирован.")')
        LoginForm().signin_to_app(self, SITE_QA_URL, email, password)
        time.sleep(2)
        self.open(SITE_QA_URL + "settings/account/")
        time.sleep(2)
        # Click the first button.
        # self.click("button")
        # self.click('a[title="Настройки"]')
        self.wait_for_element(f'div:contains("{email}"):contains("Подтвержден")')

    @pytest.mark.confirm_sign_up_with_code
    def test_sign_up_confirm_with_code(self):
        email = generate_email()
        password = get_random_string(8)
        RegisterForm().signup_to_app(self, SITE_QA_URL, email, password)
        self.click('button:contains("Вход")')
        self.wait_for_element('input[name="email"]')
        self.click('input[name="email"]')
        self.type('input[name="email"]', email)
        self.click('button[type="submit"]')
        time.sleep(7)
        code = UserData.get_auth_code()
        input_elements = self.find_elements('input[type="text"]')
        # for digit in code: # When using loop, sometimes skips one random digit
        input_elements[0].send_keys(code[0])
        input_elements[1].send_keys(code[1])
        input_elements[2].send_keys(code[2])
        input_elements[3].send_keys(code[3])
        input_elements[4].send_keys(code[4])
        self.click('button[type="submit"]')
        time.sleep(2)
        self.open(SITE_QA_URL + "settings/account/")
        # Click the first button.
        # self.click("button")
        # self.click('a[title="Настройки"]')
        # Где написано что подтвержден?
        self.wait_for_element(f'div:contains("{email}"):contains("Подтвержден")')

    @pytest.mark.sign_up_with_google
    def test_sign_up_with_google(self):
        email = generate_email()
        self.open(SITE_QA_URL)
        self.click('button:contains("Регистрация")')
        self.wait_for_element('a[href^="https://accounts.google.com/"]')
        self.click('a[href^="https://accounts.google.com/"]')
        time.sleep(3)
        self.find_element('input[type="email"]').send_keys(QA_AUTOTEST_EMAIL)
        time.sleep(2)
        self.click('input#next') # Old Google Sign In Form for headless mode
        # self.click('button:contains("Далее")') # New Google Sign In Form (Language depends on the browser settings)

        # ONLY CAN CHECK THAT LINK IS OPENED
        # BROWSERS BLOCKS THE FOLLOWING LOGIN PROCESS WITH WEBDRIVER

    @pytest.mark.sign_up_with_apple
    @pytest.mark.skip(reason="DOESN'T WORK! WAITING FOR FIX!")
    def test_sign_up_with_apple(self):
        email = generate_email()

    @pytest.mark.sign_up_with_vk
    @pytest.mark.skip(reason="DOESN'T WORK! WAITING FOR FIX")
    def test_sign_up_with_vk(self):
        email = generate_email()

    @pytest.mark.sign_up_with_telegram
    @pytest.mark.skip(reason="SKIP FOR NOW")
    def test_sign_up_with_telegram(self):
        email = generate_email()


@allure.story('SignIn')
class SignInTests(BaseCase):
    @pytest.mark.sign_in_with_pass
    def test_login_to_app(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Мои предметы")')
        self.assert_element('section:contains("Предметы")')

    @pytest.mark.sign_in_with_code
    def test_sign_in_with_code(self):
        # LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.open(SITE_QA_URL)
        self.click('button:contains("Вход")')
        self.wait_for_element('input[name="email"]')
        self.click('input[name="email"]')
        self.type('input[name="email"]', QA_AUTOTEST_EMAIL)
        self.click('button[type="submit"]')
        time.sleep(5)
        code = UserData.get_auth_code()
        input_elements = self.find_elements('input[type="text"]')
        # for digit in code: # When using loop, sometimes skips one random digit
        input_elements[0].send_keys(code[0])
        input_elements[1].send_keys(code[1])
        input_elements[2].send_keys(code[2])
        input_elements[3].send_keys(code[3])
        input_elements[4].send_keys(code[4])
        self.click('button[type="submit"]')
        time.sleep(5)
        self.assert_element('section:contains("Предметы")')

    @pytest.mark.sign_in_with_google
    def test_sign_in_with_google(self):
        email = generate_email()
        self.open(SITE_QA_URL)
        self.click('button:contains("Вход")')
        self.wait_for_element('a[href^="https://accounts.google.com/"]')
        self.click('a[href^="https://accounts.google.com/"]')
        self.find_element('input[type="email"]').send_keys(QA_AUTOTEST_EMAIL)
        time.sleep(2)
        self.click('input#next') # Old Google Sign In Form for headless mode
        # self.click('button:contains("Далее")') # New Sign In Form (Language depends on the browser settings)

        # ONLY CAN CHECK THAT LINK IS OPENED
        # BROWSERS BLOCKS THE FOLLOWING LOGIN PROCESS WITH WEBDRIVER

    @pytest.mark.sign_in_with_apple
    @pytest.mark.skip(reason="DOESN'T WORK! WAITING FOR FIX!")
    def test_sign_in_with_apple(self):
        email = generate_email()

    @pytest.mark.sign_up_with_vk
    @pytest.mark.skip(reason="DOESN'T WORK! WAITING FOR FIX")
    def test_sign_up_with_vk(self):
        email = generate_email()

    @ pytest.mark.sign_in_with_telegram
    @pytest.mark.skip(reason="SKIP FOR NOW")
    def test_sign_in_with_telegra(self):
        email = generate_email()


@allure.story('Subjects Page')
class SubjectsTests(BaseCase):
    @pytest.mark.usefixtures("delete_subscription")
    @pytest.mark.check_subjects
    # NEEDS UPDATE
    def test_subjects(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        # 1. Все курсы отображаются
        # self.assert_element('section:contains("Мои предметы")')
        self.assert_element('section:contains("Предметы")')

        self.assert_element('div#ZVCUDDES')
        # 2. Баннер курса мгновенно загружается
        # course_div = self.get_element(f'div[title="Тестовый предмет QA"]')
        time.sleep(2)
        self.assert_element('div#ZVCUDDES div.has-image')

        # 3. Кнопка "Подробнее" активна/ открывает описание курса
        self.click('div#ZVCUDDES a')
        time.sleep(2)
        self.switch_to_window(0)

        # 4. У всех курсов корректная стоимость/тариф на кнопке "Купить"
        self.assert_text("Попробовать бесплатно", 'div#ZVCUDDES span:first-child')
        self.assert_text("day - 0 $, далее 1 $", 'div#ZVCUDDES button span:last-child')

        # 5. Курсы недоступны к открытию
        # Subscribe free course in Subjects section
        self.click('div#DPBA7D3V button')
        # Open this course in MySubjects section
        self.assert_element('section:contains("Мои предметы")')
        self.click('section:contains("Мои предметы") div#DPBA7D3V button')
        self.assert_url_contains('DPBA7D3V')
        # Execute fixture after tests
        # Cancel free subject subscription by ID


@allure.story('Course Tests')
class CourseTests(BaseCase):
    @pytest.mark.buy_course_options
    def test_buy_course_options(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Предметы")')
        self.assert_element('div#MBNDBLE0') # Платный Предмет

        self.click('div#MBNDBLE0 button')

        self.assert_element('div#modal:contains("Платная подписка")')
        self.click('button:contains("Оплатить подписку")')

        # Check subscription period
        self.assert_element('div[class*="style__PreviewPeriod-"]:contains("бессрочно")')

        
        # Payment options check
        self.assert_element('div:contains("Способ оплаты")')

        # [id$="option-0"] 
        # [class*="style__PreviewPeriod-"]
        time.sleep(3)
        self.click('div#registration-order-payment')
        self.click('div#registration-order-payment div:nth-of-type(2) div div:contains("Российская банковская карта")')
        self.assert_element('div#preview-order-currency:contains("₽")')

        time.sleep(3)
        self.click('div#registration-order-payment')
        self.click('div#registration-order-payment div:nth-of-type(2) div div:contains("Visa/MasterCard")')
        self.assert_element('div#preview-order-currency:contains("$")')

        time.sleep(3)
        self.click('div#registration-order-payment')
        self.click('div#registration-order-payment div:nth-of-type(2) div div:contains("Криптовалюта")')
        self.assert_element('div#preview-order-currency:contains("$")')


    @pytest.mark.buy_course_rus_card
    def test_buy_course_rus_card(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Предметы")')
        self.assert_element('div#MBNDBLE0') # Платный Предмет

        self.click('div#MBNDBLE0 button')
        self.assert_element('div#modal:contains("Платная подписка")')
        self.click('button:contains("Оплатить подписку")')
        time.sleep(3)

        self.click('div#registration-order-payment')
        self.click('div#registration-order-payment div:nth-of-type(2) div div:contains("Российская банковская карта")')
        time.sleep(5)

        self.assert_element('div#ru-cards-new:contains("Новая карта")')
        time.sleep(5)
        self.click('div#ru-cards-new') 
        time.sleep(5)

        # self.find_element('input[name="card_number"]').send_keys("2202202202202200")
        test_card = {'card': CARD_NUMBER, "month": "01", "year": "30", 'cvv': '123'}
        self.type('input[name="card_number"]', test_card['card'])
        self.type('input[name="cvv"]', test_card['cvv'])
        self.type('input[name="exp_date_month"]', test_card['month'])
        self.type('input[name="exp_date_year"]', test_card['year'])

        self.click('span[class^="style__Checkmark"]')
        time.sleep(2)

        self.click('button:contains("Оплатить")')
        time.sleep(5)
        self.assert_url_contains('cloudpayments')

    @pytest.mark.buy_course_saved_rus_card
    def test_buy_course_saved_rus_card(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Предметы")')
        self.assert_element('div[title="ПЛАТНЫЙ ПРЕДМЕТ QA"]')

        self.click('div[title="ПЛАТНЫЙ ПРЕДМЕТ QA"] button')
        self.assert_element('div#modal:contains("Платная подписка")')
        self.click('button:contains("Оплатить подписку")')
        time.sleep(3)

        self.click('div input')
        self.click('div:contains("Российская банковская карта")')
        self.assert_element('div:contains("Мои карты")')

        self.click('div:contains("Новая карта")')
        # No cards added

    @pytest.mark.buy_course_visa_master
    def test_buy_course_visa_master(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Предметы")')
        self.assert_element('div#MBNDBLE0')  # Платный Предмет

        self.click('div#MBNDBLE0 button')

        self.assert_element('div#modal:contains("Платная подписка")')
        self.click('button:contains("Оплатить подписку")')


        self.click('div#registration-order-payment')
        self.click('div#registration-order-payment div:nth-of-type(2) div div:contains("Visa/MasterCard")')
        self.click('button:contains("Перейти к оплате")')

        time.sleep(5)

        self.assert_url_contains('https://pay.pulpal.az/')
        self.wait_for_element_absent('app-error-conf-page', by="css selector", timeout=None)

        # PULPAL PAYMENT WORKFLOW BELOW
        # Input RUS card number and other fields
        # card = self.find_element('input[name="card_number"]')
        # card_cvv = self.find_element('input[name="cvv"]')
        # expire_month = self.find_element('input[name="exp_date_month"]')
        # expire_year = self.find_element('input[name="exp_date_year"]')
        # test_card = {'card': CARD_NUMBER,"month": "01", "year": "30", 'cvv': '123'}
        # card.send_keys(test_card['card'])
        # expire_month.send_keys(test_card['card'])
        # expire_year.send_keys(test_card['card'])
        # card_cvv.send_keys(test_card['card'])

    @pytest.mark.buy_course_crypto
    def test_buy_course_crypto(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Предметы")')
        self.assert_element('div#MBNDBLE0') # Платный Предмет

        self.click('div#MBNDBLE0 button')

        self.assert_element('div#modal:contains("Платная подписка")')
        self.click('button:contains("Оплатить подписку")')


        self.click('div#registration-order-payment')
        self.click('div#registration-order-payment div:nth-of-type(2) div div:contains("Криптовалюта")')
        self.click('button:contains("Перейти к оплате")')

        self.assert_url_contains('https://pay.usegateway.net/payments/')
        time.sleep(3)
        self.assert_element('h2[class^="header__HeaderTitle"]:contains("ПЛАТНЫЙ ПРЕДМЕТ QA")')


    @pytest.mark.usefixtures("gift_a_subscription", "delete_subscription_after")
    @pytest.mark.course_unsubscribe
    def test_course_unsubscribe(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Мои предметы")')
        self.assert_element('section:contains("Предметы")')

        # Click the first button.
        # self.click("button")
        # self.click('a[title="Настройки"]')

        self.open(SITE_QA_URL + "settings/payment/")
        time.sleep(2)
        
        # Check name 
        # Check date
        # class="styles__SubscriptionTitleInfo
        # self.assert_element(f'div:contains("КУРС ДЛЯ ОТПИСКИ QA")')
        self.assert_element('div[class^="styles__SubscriptionTitleInfo"] label:contains("КУРС ДЛЯ ОТПИСКИ QA")')
        next_date_payment =  (date.today() + timedelta(days=30)).strftime('%d %b. %Y')
        # self.assert_element('div[class^="styles__SubscriptionTitleInfo"] p:contains("Дата следующего списания: 23 июл. 2023")')  # UPDATE
    
        # Cancell subscription
        self.click('button:contains("Отмена")')
        self.click('button[type="submit"]')
        time.sleep(3)
        self.click('button span:contains("OK")')
        time.sleep(3)
        self.refresh_page() 
        time.sleep(3)

        # Check date info after cancell
        # self.assert_element('div[class^="styles__SubscriptionTitleInfo"] p:contains("Активна до: 23 июл. 2023")')  # UPDATE


        self.assert_element('button:contains("Возобновить")')

        # Check the course in the MySubjects Section

        # Remove subscription

        # 1. Покупка курса успешно отменяется
        # 2. Курс доступен до конца даты указанного тарифа
        # 3. Последующее списание средств не происходит


@ allure.story('Course Quality Tests')
class CourseQualityTests(BaseCase):

    @pytest.mark.skip()
    @pytest.mark.course_quality
    def test_course_quality(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Мои предметы")')
        self.assert_element('section:contains("Предметы")')

    # 1. Наполнение курса соответствует плану обучения
    # 2. В теории/тезисах/вопросах нет ошибок
    # 3. Все видео воспроизводится/есть возможность открыть полноэкранный просмотр
    # 4. Чат-бот работает корректно
    # 5. Все ссылки/формы обратной связи активны и актуальны


@allure.story('Feedback Tests')
class FeebackTests(BaseCase):
    @pytest.mark.feedback_form
    def test_feedback_form(self):
        LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
        self.assert_element('section:contains("Мои предметы")')
        self.assert_element('section:contains("Предметы")')

        self.scroll_to_bottom()
        self.assert_element('a[title="Telegram"]')
        self.click('a[title="Telegram"]')
        time.sleep(5)
        self.switch_to_window(1) # works this way for headless mode (on remote server)
        time.sleep(2)
        self.assert_url_contains(TELEGRAM_LINK)
        self.assert_element('div[class="tgme_page"]:contains("CyberYozh")', timeout=10)
        self.switch_to_window(0)
        self.click('button:contains("Поддержка")', timeout=10)
        self.is_element_visible('div#modal form')
        time.sleep(3)
        self.assert_exact_text(QA_AUTOTEST_EMAIL, 'div#modal form input[name="email"]')

        themes = ["Ошибка в видео или упражнении", "Технические проблемы", "Ошибка/уязвимость", "Предложить сотрудничество", "Другие вопросы"]

        for theme in themes:
            self.click('div#modal form div:nth-of-type(2)', timeout=10)
            time.sleep(1)
            self.click(f'div#react-select-2-listbox div div:contains("{theme}")', timeout=10)
            time.sleep(1)
            self.assert_element(f'div#modal form div:nth-of-type(2):contains("{theme}")', timeout=10)

        self.assert_element('div#modal form div:nth-of-type(3) div div textarea[name="description"]')
        self.click('div#modal form div:nth-of-type(3) div div textarea[name="description"]')
        random_text = "Случайное сообщение о проблеме пользователя. Все сломалось, ничего не работает, верните деньги!"
        self.type('div#modal form div:nth-of-type(3) div div textarea[name="description"]', random_text)

        self.choose_file('div#modal form input[type="file"]', 'test_files/test_pic.jpeg') 
  
        time.sleep(2)

        self.click('div#modal form button[type="submit"]')
        time.sleep(3)
        self.assert_element('div#modal:contains("Ваше сообщение успешно отправлено. Служба поддержки свяжется с вами в ближайшее время по email.")')
        self.click('div#modal button')