import allure
import pytest
import time
from datetime import date, timedelta
from pytest_steps import test_steps
from seleniumbase import BaseCase
from selenium.webdriver.common.action_chains import ActionChains

from site_apis.user.model import *

from pages.register_auth_form import *

from constants import SITE_QA_URL, QA_AUTOTEST_EMAIL, SITE_HEADER, QA_PASSWORD, TELEGRAM_BOT_LINK

# Helper functions/data
accept = {"Accept": SITE_HEADER}


class Register:
    def signup_to_app(self, sb, url, login, password):
        sb.open(url)
        sb.click(RegisterForm.REGISTRATION_BUTTON)
        sb.wait_for_element('input[name="login"]')
        sb.wait_for_element('input[name="password"]')
        sb.click('input[name="login"]')
        sb.type('input[name="login"]', login)
        sb.click('input[name="password"]')
        sb.type('input[name="password"]', password)
        sb.click('input[type="checkbox"] + span')
        sb.click('button[type="submit"]')

    def click_registration_button(self, sb):
        sb.open(SITE_QA_URL)
        sb.click(RegisterForm.REGISTRATION_BUTTON) 

    def click_auth_button(self, sb):
        sb.open(SITE_QA_URL)
        sb.click(RegisterForm.AUTH_BUTTON)

    def check_error_messages(self, sb, error_elements):
        for error_element in error_elements:
            if error_elements.index(error_element) == 0:
                sb.assertEqual(error_element.text, "Укажите правильный адрес эл. почты")
            else:
                sb.assertEqual(error_element.text, "Пароль должен быть не менее 8 символов")

            color = error_element.value_of_css_property("color")
            sb.assertEqual(color, "rgba(255, 58, 52, 1)")

        # Div Input Selectors
        div_input_selectors = [RegisterForm.DIV_EMAIL_INPUT, RegisterForm.DIV_PASSWORD_INPUT]

        for selector in div_input_selectors:
            div_element_input = sb.find_element(selector) 
            border_style = div_element_input.value_of_css_property("border")
            sb.assertEqual(border_style, "1px solid rgb(255, 58, 52)")

    def check_email_input(self, sb, input_element):
        input_field = sb.find_element(input_element) # RegisterForm.EMAIL_INPUT
        sb.click(input_element)
        # Cursor is active
        actions = ActionChains(sb.driver)
        actions.move_to_element(input_field)
        actions.perform()
        time.sleep(3)
        focused_element = sb.driver.switch_to.active_element
        sb.assertEqual(focused_element, input_field)
        # Placeholder becomes smaller and position above cursor
        placeholder_element = sb.find_element(RegisterForm.EMAIL_INPUT_LABEL) 
        transform_property = placeholder_element.value_of_css_property("transform")
        sb.assertEqual(transform_property, "matrix(0.75, 0, 0, 0.75, 16, 0)") # Assert that transform_property property is changed


@allure.story('Open Registration Form')
class OpenRegistration(BaseCase):
    @pytest.mark.open_registration_form
    def test_open_registration_form(self):
        Register().click_registration_button(self)
        element = self.find_element(RegisterForm.REGISTER_FORM_BUTTON)  
        font_size = element.value_of_css_property("font-size")
        self.assertEqual(font_size, "24px") # Assert Registration Form is opened and active   

@allure.story('Registration Form')
class RegistrationForm(BaseCase):
    @pytest.mark.click_email_input
    def test_click_email_input(self):
        Register().click_registration_button(self)
        Register().check_email_input(self, RegisterForm.EMAIL_INPUT)
        
    @pytest.mark.input_valid_email
    def test_input_valid_email(self):
        Register().click_registration_button(self)
        email = generate_email()

        input_type = self.get_attribute(RegisterForm.EMAIL_INPUT, "type")

        self.type(RegisterForm.EMAIL_INPUT, email)
        email_value = self.get_attribute(RegisterForm.EMAIL_INPUT, "value")
        
        self.assertEqual(input_type, 'text')
        self.assertEqual(email_value, email) # Data is present in the input
        # The Input is framed with blue color


    @pytest.mark.click_password_input
    def test_click_password_input(self):
        Register().click_registration_button(self)

        input_field = self.find_element(RegisterForm.PASSWORD_INPUT)
        self.click(RegisterForm.PASSWORD_INPUT)
        # Cursor is active
        actions = ActionChains(self.driver)
        actions.move_to_element(input_field)
        actions.perform()
        time.sleep(3)
        focused_element = self.driver.switch_to.active_element
        self.assertEqual(focused_element, input_field)
        # Placeholder becomes smaller and position above cursor
        placeholder_element = self.find_element(RegisterForm.PASSWORD_INPUT_LABEL) 
        transform_property = placeholder_element.value_of_css_property("transform")
        self.assertEqual(transform_property, "matrix(0.75, 0, 0, 0.75, 16, 0)") # Assert that transform_property property is changed
        
    @pytest.mark.input_valid_password
    def test_input_valid_password(self):
        Register().click_registration_button(self)
        password = get_random_string(8)

        input_type = self.get_attribute(RegisterForm.PASSWORD_INPUT, "type")

        self.type(RegisterForm.PASSWORD_INPUT, password)
        password_value = self.get_attribute(RegisterForm.PASSWORD_INPUT, "value")

        self.assertEqual(input_type, 'password') # Data is present in the input as a dots
        self.assertEqual(password_value, password) # Data is present in the input
        self.assertGreaterEqual(len(password_value), 8) # Input 8 symbols or more


    # @pytest.mark.sign_in_with_valid_data
    # def test_login_to_app(self):
    #     LoginForm().signin_to_app(self, SITE_QA_URL, QA_AUTOTEST_EMAIL, QA_PASSWORD)
    #     self.assert_element('section:contains("Мои предметы")')
    #     self.assert_element('section:contains("Предметы")')

    @pytest.mark.click_register_with_empty_fields
    def test_click_register_with_empty_fields(self):
        Register().click_registration_button(self)
        
        self.click(RegisterForm.CHECK_BOX)
        self.click(RegisterForm.SUBMIT_BUTTON)
        time.sleep(3)

        # Error Elements
        error_elements = self.find_elements(RegisterForm.INPUT_ERROR)

        # Complete all checks
        Register().check_error_messages(self, error_elements)


    @pytest.mark.click_register_with_invalid_email
    def test_click_register_with_invalid_email(self):
        Register().click_registration_button(self)
        email = 'random_string@.com'
        password = get_random_string(8)
        time.sleep(2)

        self.type(RegisterForm.EMAIL_INPUT, email)
        self.type(RegisterForm.PASSWORD_INPUT, password)

        self.click(RegisterForm.CHECK_BOX)
        self.click(RegisterForm.SUBMIT_BUTTON)
        time.sleep(2)

        error_element = self.find_element(RegisterForm.INPUT_ERROR)

        self.assertEqual(error_element.text, "Укажите правильный адрес эл. почты")

        color = error_element.value_of_css_property("color")
        self.assertEqual(color, "rgba(255, 58, 52, 1)")

        div_element_input = self.find_element(RegisterForm.DIV_EMAIL_INPUT) 
        border_style = div_element_input.value_of_css_property("border")
        self.assertEqual(border_style, "1px solid rgb(255, 58, 52)")



    
    @pytest.mark.click_register_with_invalid_password
    def test_click_register_with_invalid_password(self):
        Register().click_registration_button(self)
        email = generate_email()
        password = 'asnnb)-8_**#@#_@#&@#Cljваыовжж2'
        time.sleep(2)

        self.type(RegisterForm.EMAIL_INPUT, email)
        self.type(RegisterForm.PASSWORD_INPUT, password)

        self.click(RegisterForm.CHECK_BOX)
        self.click(RegisterForm.SUBMIT_BUTTON)
        time.sleep(2)

        error_element = self.find_element(RegisterForm.INPUT_ERROR)
        
        self.assertEqual(error_element.text, "Максимальное количество символов 30")

        color = error_element.value_of_css_property("color")
        self.assertEqual(color, "rgba(255, 58, 52, 1)")

        div_element_input = self.find_element(RegisterForm.DIV_PASSWORD_INPUT) 
        border_style = div_element_input.value_of_css_property("border")
        self.assertEqual(border_style, "1px solid rgb(255, 58, 52)")


    @pytest.mark.click_register_with_invalid_fields
    def test_click_register_with_invalid_fields(self):
        Register().click_registration_button(self)
        email = 'random_string@.com'
        password = 'asnnb)-'

        time.sleep(2)

        self.type(RegisterForm.EMAIL_INPUT, email)
        self.type(RegisterForm.PASSWORD_INPUT, password)

        self.click(RegisterForm.CHECK_BOX)
        self.click(RegisterForm.SUBMIT_BUTTON)
        time.sleep(3)

        # Error Elements
        error_elements = self.find_elements(RegisterForm.INPUT_ERROR)
        # Complete all checks
        Register().check_error_messages(self, error_elements)


    
    @pytest.mark.show_password
    def test_show_password(self):
        Register().click_registration_button(self)
        password = get_random_string(8)
        self.type(RegisterForm.PASSWORD_INPUT, password)

        self.click(RegisterForm.TOGGLE_PASSWORD)

        input_type = self.get_attribute(RegisterForm.PASSWORD_INPUT, "type")
        self.assertEqual(input_type, 'text')

    @pytest.mark.hide_password
    def test_hide_password(self):
        Register().click_registration_button(self)
        password = get_random_string(8)
        self.type(RegisterForm.PASSWORD_INPUT, password)

        self.click(RegisterForm.TOGGLE_PASSWORD) # show password
        self.click(RegisterForm.TOGGLE_PASSWORD) # hide password

        input_type = self.get_attribute(RegisterForm.PASSWORD_INPUT, "type")
        self.assertEqual(input_type, 'password')

    @pytest.mark.checkbox_is_marked
    def test_checkbox_is_marked(self):
        Register().click_registration_button(self)

        element = self.find_element(RegisterForm.SUBMIT_BUTTON)
        submit_button_enabled = element.value_of_css_property("disabled")

        self.click(RegisterForm.CHECK_BOX)

        check_box_fill = self.get_attribute(RegisterForm.SVG_CHECK_BOX, "fill")
        self.assertEqual(check_box_fill, "white")
        self.assertEqual(submit_button_enabled, "")


    @pytest.mark.click_google
    def test_click_google(self):
        Register().click_registration_button(self)
        self.click(RegisterForm.GOOGLE_AUTH_LINK)
        time.sleep(3)
        self.assert_url_contains('https://accounts.google.com/v3/signin/')


    @pytest.mark.skip(reason="DOESN'T WORK! WAITING FOR FIX")
    @pytest.mark.click_apple
    def test_click_apple(self):
        Register().click_registration_button(self)
        self.click(RegisterForm.APPLE_AUTH_LINK)

    @pytest.mark.click_vk
    def test_click_vk(self):
        Register().click_registration_button(self)
        self.click(RegisterForm.VK_AUTH_LINK)

    @pytest.mark.click_telegram
    def test_click_telegram(self):
        Register().click_registration_button(self)
        self.click(RegisterForm.TELEGRAM_AUTH_LINK)
        time.sleep(3)
        self.assert_url_contains(TELEGRAM_BOT_LINK)



@allure.story('Open Authorization Form')
class OpenAuthorization(BaseCase):
    @pytest.mark.open_auth_form
    def test_open_auth_form(self):
        Register().click_auth_button(self)
        time.sleep(5)
        element = self.find_element(RegisterForm.AUTH_FORM_BUTTON)  
        font_size = element.value_of_css_property("font-size")
        self.assertEqual(font_size, "24px") # Assert Registration Form is opened and active


@allure.story('Authorization Form')
class AuthorizationForm(BaseCase):
    @pytest.mark.click_auth_email_input
    def test_click_auth_email_input(self):
        Register().click_auth_button(self)
        Register().check_email_input(self, AuthForm.EMAIL_INPUT)


    @pytest.mark.input_auth_valid_email
    def test_input_auth_valid_email(self):
        Register().click_auth_button(self)
        email = generate_email()

        input_type = self.get_attribute(AuthForm.EMAIL_INPUT, "type")

        self.type(AuthForm.EMAIL_INPUT, email)
        email_value = self.get_attribute(AuthForm.EMAIL_INPUT, "value")
        
        self.assertEqual(input_type, 'text')
        self.assertEqual(email_value, email) # Data is present in the input
        # The Input is framed with blue color

    @pytest.mark.click_get_code_valid_email
    def test_click_get_code_valid_email(self):
        Register().click_auth_button(self)

        self.type(AuthForm.EMAIL_INPUT, QA_AUTOTEST_EMAIL) 
        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(3)

        # Get Code
        code = UserData.get_auth_code()
        self.assertIsNotNone(code)


    @pytest.mark.click_get_code_empty_email
    def test_click_get_code_empty_email(self):
        Register().click_auth_button(self)

        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(2)
        
        error_element = self.find_element(AuthForm.INPUT_ERROR)
        self.assertEqual(error_element.text, "Поле не может быть пустым")

        color = error_element.value_of_css_property("color")
        self.assertEqual(color, "rgba(255, 58, 52, 1)")

        div_element_input = self.find_element(AuthForm.DIV_EMAIL_INPUT)
        border_style = div_element_input.value_of_css_property("border")
        self.assertEqual(border_style, "1px solid rgb(255, 58, 52)")


    @pytest.mark.click_get_code_invalid_email
    def test_click_get_code_invalid_email(self):
        Register().click_auth_button(self)

        email = 'random_string@.com'
        self.type(AuthForm.EMAIL_INPUT, email)

        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(2)
        
        error_element = self.find_element(AuthForm.INPUT_ERROR)
        self.assertEqual(error_element.text, "Укажите правильный адрес эл. почты")

        color = error_element.value_of_css_property("color")
        self.assertEqual(color, "rgba(255, 58, 52, 1)")

        div_element_input = self.find_element(AuthForm.DIV_EMAIL_INPUT)
        border_style = div_element_input.value_of_css_property("border")
        self.assertEqual(border_style, "1px solid rgb(255, 58, 52)")

    @pytest.mark.open_auth_with_password_form
    def test_open_auth_with_password_form(self):
        Register().click_auth_button(self)
        self.click(AuthForm.AUTH_WITH_PASS_SPAN)
        time.sleep(2)

        element = self.find_element(AuthForm.AUTH_TITLE)  
        font_size = element.value_of_css_property("font-size")
        self.assertEqual(font_size, "28px") # Assert Authorization Form is opened and active

        input_value = self.get_attribute(AuthForm.LOGIN_INPUT, "value")
        self.assertEqual(input_value, '')
        self.assert_element(AuthForm.PASSWORD_INPUT)


@allure.story('Input Confirmation Code Pop Up')
class ConfirmationCode(BaseCase):
    @pytest.mark.click_empty_confirm_code
    def test_click_empty_confirm_code(self):
        Register().click_auth_button(self)
        self.click(AuthForm.AUTH_WITH_PASS_SPAN)
        time.sleep(2)

        self.type(AuthForm.EMAIL_INPUT, QA_AUTOTEST_EMAIL)
        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(2)

        self.click(ConfirmCodeForm.CONFIRM_CODE_BUTTON)


    @pytest.mark.click_invalid_confirm_code
    def test_click_invalid_confirm_code(self):
        Register().click_auth_button(self)

        self.type(AuthForm.EMAIL_INPUT, QA_AUTOTEST_EMAIL)
        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(1)

        input_elements = self.find_elements(ConfirmCodeForm.CODE_INPUT)
        input_elements[0].send_keys(1)
        self.click(ConfirmCodeForm.CONFIRM_CODE_BUTTON)
        time.sleep(1)

        # ASSERT SHAKKING EFFECT
        class_value = self.get_attribute(ConfirmCodeForm.CODE_INPUT, "class")
        self.assertEqual(class_value, "shakeX") # Assert Shaking of the input cells

        error_element = self.find_element(ConfirmCodeForm.CODE_ERROR)
        self.assertEqual(error_element.text, "Неверный код авторизации.")

        color = error_element.value_of_css_property("color")
        self.assertEqual(color, "rgba(255, 58, 52, 1)")

    @pytest.mark.click_valid_confirm_code
    def test_click_valid_confirm_code(self):
        Register().click_auth_button(self)

        self.type(AuthForm.EMAIL_INPUT, QA_AUTOTEST_EMAIL)
        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(3)

        code = UserData.get_auth_code()


        input_elements = self.find_elements(ConfirmCodeForm.CODE_INPUT)
        input_elements[0].send_keys(code[0])
        input_elements[1].send_keys(code[1])
        input_elements[2].send_keys(code[2])
        input_elements[3].send_keys(code[3])
        input_elements[4].send_keys(code[4])
    
        self.click(ConfirmCodeForm.CONFIRM_CODE_BUTTON)
        time.sleep(3)
        self.assert_element('section:contains("Предметы")')


    @pytest.mark.open_auth_with_password_form_code_page
    def test_open_auth_with_password_form_code_page(self):
        Register().click_auth_button(self)
        self.type(AuthForm.EMAIL_INPUT, QA_AUTOTEST_EMAIL)
        self.click(AuthForm.GET_CODE_BUTTON)
        time.sleep(2)
        
        self.click(AuthForm.AUTH_WITH_PASS_SPAN)
        time.sleep(3)

        element = self.find_element(AuthForm.AUTH_TITLE)  
        font_size = element.value_of_css_property("font-size")
        self.assertEqual(font_size, "28px") # Assert Authorization Form is opened and active


        input_value = self.get_attribute(AuthForm.LOGIN_INPUT, "value")
        self.assertEqual(input_value, QA_AUTOTEST_EMAIL)
        self.assert_element(AuthForm.PASSWORD_INPUT)

  