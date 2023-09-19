from constants import TELEGRAM_BOT_LINK

class RegisterForm:
    FORM_SELECTOR = 'div#modal'
    REGISTRATION_BUTTON = 'button:contains("Регистрация")'
    AUTH_BUTTON = 'button:contains("Вход")'

    AUTH_FORM_BUTTON = FORM_SELECTOR + ' button:contains("Вход")'
    REGISTER_FORM_BUTTON = FORM_SELECTOR + ' button:contains("Регистрация")'

    EMAIL_INPUT = 'input[name="login"]'
    EMAIL_INPUT_LABEL = 'label:contains("Электронная почта")'
    INPUT_ERROR = 'span[class^="styles__InputError"]'
    DIV_EMAIL_INPUT = f'div:has(> {EMAIL_INPUT})'
    
    PASSWORD_INPUT = 'input[name="password"]'
    PASSWORD_INPUT_LABEL = 'label:contains("Пароль")'
    DIV_PASSWORD_INPUT = f'div:has(> {PASSWORD_INPUT})'
    TOGGLE_PASSWORD = 'span[class^="styles__InputTogglePassword"]'

    CHECK_BOX = 'input[type="checkbox"] + span'
    SVG_CHECK_BOX = 'svg[class^="check__SvgCheck"]' 
    SUBMIT_BUTTON = 'button[type="submit"]'

    GOOGLE_AUTH_LINK = 'a[href^="https://accounts.google.com/"]'
    APPLE_AUTH_LINK = ''
    VK_AUTH_LINK = ''
    TELEGRAM_AUTH_LINK = f'a[href="{TELEGRAM_BOT_LINK}"]' 

class AuthForm:
    AUTH_BUTTON=""
    AUTH_WITH_PASS_SPAN = 'span[class^="styles__SignInBottomLink"]'
    EMAIL_INPUT = 'input[name="email"]'
    PASSWORD_INPUT = 'input[name="password"]'
    GET_CODE_BUTTON = 'button[type="submit"]'
    INPUT_ERROR = 'span[class^="styles__InputError"]'
    DIV_EMAIL_INPUT = f'div:has(> {EMAIL_INPUT})'

    AUTH_TITLE = 'h2:contains("Войти в аккаунт")'
    LOGIN_INPUT = 'input[name="login"]'


class ConfirmCodeForm:
    CODE_INPUT = 'input[type="text"]'
    CONFIRM_CODE_BUTTON = 'button[type="submit"]'
    CODE_ERROR = 'ul[class^="styles__NonFieldErrorsList"] li'
    AUTH_WITH_PASS_SPAN = 'span[class^="styles__SignInBottomLink"]'
