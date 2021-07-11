import os
abs_path = os.path.abspath(os.path.dirname(__file__))

############################
#                          #
# !WARNING SENSITIVE INFO! #
#                          #
############################


class Config(object):
    # ------ FLASK ------ #
    DEBUG = False
    TESTING = False

    # ------ CDN ------ #
    CDN_FTP_ADDRESS = 'nl01.upload.cdn13.com'
    CDN_FTP_USERNAME = '1011335.1011335'
    CDN_FTP_PASSWORD = 'gTmUjIMaeCgQiTQM'
    CDN_DIR_BLOG = '/blog/'

    # ------ Directory ------ #
    TEMPLATES_FOLDER = os.path.join(abs_path, 'app', 'public', 'dist', 'templates')
    EMAIL_TEMPLATES_FOLDER = os.path.join(TEMPLATES_FOLDER, 'emails')
    STATIC_FOLDER = os.path.join(abs_path, 'app', 'public', 'dist', 'assets')
    TEMP_UPLOAD_FOLDER = os.path.join(abs_path, 'app', 'public', 'dist', 'assets')

    # ------ Settings ------ #
    SUPERUSERS = ['']
    ADMINS = ['']
    ERRORS_MAIL = ''
    MAIL_FORM_RECIPIENT = ''
    BLOG_POSTS_PER_PAGE = 2
    BLOG_THUMBNAIL_SIZE = (1280, 720)

    # ------ Messages ------ #
    MSG_EXAMPLE = ''

    # ------ SQLALCHEMY ------ #
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ------ Flask-Admin ------ #
    FLASK_ADMIN_SWATCH = 'flatly'
    FLASK_ADMIN_FLUID_LAYOUT = True

    # ------ SECURITY ------ #
    SECURITY_PASSWORD_SALT = '!)D*$b;@%a_9o;AG^W2(:=F=bo;:`d=L'
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_EMAIL_SENDER = 'office@powersoft.bg'
    SECURITY_EMAIL_PLAINTEXT = False
    SECURITY_LOGIN_URL = '/login/'
    SECURITY_LOGOUT_URL = '/logout/'
    SECURITY_REGISTER_URL = '/signup/'
    SECURITY_RESET_URL = '/reset-password/'
    SECURITY_CHANGE_URL = '/change-password/'
    SECURITY_CONFIRM_URL = '/confirm-email/'
    SECURITY_POST_LOGIN_VIEW = '/login/'
    SECURITY_POST_CONFIRM_VIEW = '/login/'
    SECURITY_POST_CHANGE_VIEW = '/login/'
    SECURITY_POST_RESET_VIEW = '/'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_UNAUTHORIZED_VIEW = '/'
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/signup.html'
    SECURITY_FORGOT_PASSWORD_TEMPLATE = 'security/forgot_password.html'
    SECURITY_RESET_PASSWORD_TEMPLATE = 'security/reset_password.html'
    SECURITY_CHANGE_PASSWORD_TEMPLATE = 'security/change_password.html'
    SECURITY_SEND_CONFIRMATION_TEMPLATE = 'security/send_confirmation.html'
    SECURITY_EMAIL_SUBJECT_REGISTER = 'Добре дошъл!'
    SECURITY_EMAIL_SUBJECT_CONFIRM = 'Моля потвърди своя имейл'
    SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = 'Тоята парола беше променена'
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = 'Инструцкии за промяна на паролата'
    SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = 'Твоята парола беше променена'
    SECURITY_MSG_CONFIRM_REGISTRATION = ('Акаунтът е направен успешно. Инструкции за потвърждаване на имейла бяха пратени на %(email)s.', 'success')
    SECURITY_MSG_ALREADY_CONFIRMED = ('Имейлът вече е потвърден.', 'info')
    SECURITY_MSG_ANONYMOUS_USER_REQUIRED = ('Тази страница може да бъде достъпена само ако не сте влезли в акаунта си.', 'error')
    SECURITY_MSG_CONFIRMATION_EXPIRED = ('Тъй като имейлът не беше потвърден в рамките на %(within)s, нов имейл за потвърждение беше изпратен на %(email)s."', 'error')
    SECURITY_MSG_CONFIRMATION_REQUEST = ('Имейл за подтвърждение беше изпратен на %(email)s.', 'success')
    SECURITY_MSG_CONFIRMATION_REQUIRED = ('Имейлът трябва да бъде потвърден.', 'error')
    # SECURITY_MSG_CONFIRM_REGISTRATION = ('Thank you. Confirmation instructions have been sent to %(email)s. If you haven\'t received a confirmation email you can <a href="/confirm-email/">resend</a> the link.', 'success')
    SECURITY_MSG_DISABLED_ACCOUNT = ('Този акаунт е затворен.', 'error')
    SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = ('Вече съществува акаунт с този имейл.', 'error')
    SECURITY_MSG_EMAIL_CONFIRMED = ('Имейлът беше потвърден успешно.', 'success')
    SECURITY_MSG_EMAIL_NOT_PROVIDED = ('Моля въведете имейл.', 'error')
    SECURITY_MSG_FORGOT_PASSWORD = ('Забравил си паролата си?', 'info')
    SECURITY_MSG_INVALID_CONFIRMATION_TOKEN = ('Невалиден токен.', 'error')
    SECURITY_MSG_INVALID_EMAIL_ADDRESS = ('Невалиден имейл адрес.', 'error')
    SECURITY_MSG_USER_DOES_NOT_EXIST = ('Грешен имейл или парола.', 'error')
    SECURITY_MSG_INVALID_PASSWORD = ('Грешен имейл или парола.', 'error')
    SECURITY_MSG_INVALID_REDIRECT = ('Препрадки извън домейна са забранени.', 'error')
    SECURITY_MSG_INVALID_RESET_PASSWORD_TOKEN = ('Невалиден токен.', 'error')
    SECURITY_MSG_LOGIN = ('Моля влез в акаунта си, за да видиш тази страница.', 'error')
    SECURITY_MSG_PASSWORD_BREACHED = ('Тази парола е била компрометирана.', 'error')
    SECURITY_MSG_PASSWORD_BREACHED_SITE_ERROR = ('Свързването с уебсайта за компрометирани пароли беше неуспешно.', 'error')
    SECURITY_MSG_PASSWORD_CHANGE = ('Паролата е сменена успешно.', 'success')
    SECURITY_MSG_PASSWORD_INVALID_LENGTH = ('Паролата трябва да е минимум %(length)s знака.', 'error')
    SECURITY_MSG_PASSWORD_IS_THE_SAME = ('Новата ти парола трябва да е различна от старата.', 'error')
    SECURITY_MSG_PASSWORD_MISMATCH = ('Паролите не съвпадат.', 'error')
    SECURITY_MSG_PASSWORD_NOT_PROVIDED = ('Моля въведете парола.', 'error')
    SECURITY_MSG_PASSWORD_NOT_SET = ('Няма парола за този акаунт. Най-вероятно си използвал Google или Facebook.', 'error')
    SECURITY_MSG_PASSWORD_RESET = ('Паролата ти беше променена успешно.', 'success')
    SECURITY_MSG_PASSWORD_RESET_EXPIRED = ('Тъй като не възстанови паролата си в рамките на %(within)s, нов имейл с инструкции беше изпратен на %(email)s.', 'error')
    SECURITY_MSG_PASSWORD_RESET_REQUEST = ('Инструкции за възстановяване на паролата бяха изпратени на %(email)s.', 'error')
    SECURITY_MSG_PASSWORD_TOO_SIMPLE = ('Паролта е прекалено проста.', 'error')
    SECURITY_MSG_RETYPE_PASSWORD_MISMATCH = ('Паролите не съвпадат.', 'error')
    SECURITY_MSG_UNAUTHORIZED = ('Нямаш достъп до тази страница.', 'error')
    SECURITY_MSG_UNAUTHENTICATED = ('Не си влязъл в акаунта си. Моля въведи правилни данни.', 'error')


class ProductionConfig(Config):
    # ------ Flask ------ #
    DEBUG = False
    Testing = False
    SECRET_KEY = '3d59b6924697c3a8e94e4a59b9dc835aa2635940c01051abb3977167b8bf95fa'
    SERVER_NAME = 'bqlatastaq.com:443'

    # ------ Security ------ #
    SECURITY_PASSWORD_SALT = 'G>HA"6nu]uTZ9uZJYk6=wA@TXx]\Yj.6'

    # ------ CDN ------ #
    CDN_URL = ''
    CDN_FTP_DIR_MAIN = '//'
    CDN_FTP_DIR_BLOG = CDN_FTP_DIR_MAIN + 'blog/'

    # ------ Sqlalchemy ------ #
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_username:db_password@bg1.pgsqlserver.com/db_name'

    # ------ MAIL ------ #
    MAIL_SERVER = 'mail.supremecluster.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # ------ ELASTICSEARCH ------ #
    ELASTICSEARCH_URL = ''
    INDICES_POSTFIX = '_requests'  # Needed for auto creation indices when using bonsai

    # ------ PAYMENT ------ #
    PAYMENT_CHECKOUT_URL = 'https://mypos.eu/vmp/checkout/'
    PAYMENT_PRIVATE_KEY = '''
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
'''
    PAYMENT_PUBLIC_CERTIFICATE = '''
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
'''
    PAYMENT_WALLET_NUMBER = ''
    PAYMENT_STORE_ID = ''
    PAYMENT_KEY_INDEX = 1


class DevelopmentConfig(Config):
    # ------ Flask ------ #
    DEBUG = True
    SECRET_KEY = 'e6939cf258fac8d55393cd7586d576344f3037449097685a7e72898212a0f3ed'

    # ------ Security ------ #
    SECURITY_PASSWORD_SALT = ''

    # ------ CDN ------ #
    CDN_URL = 'https://11335-7.b.cdn12.com'
    CDN_FTP_DIR_MAIN = '/powersoft_test/'
    CDN_FTP_DIR_BLOG = CDN_FTP_DIR_MAIN + 'blog/'

    # ------ Sqlalchemy ------ #
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/powersoft'

    # ------ Mail ------ #
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = '7f10e14c7f7c32'
    MAIL_PASSWORD = 'ed5a92593a4a8d'

    # ------ ELASTICSEARCH ------ #
    ELASTICSEARCH_URL = 'http://localhost:9200'
    INDICES_POSTFIX = False

    # ------ Payment ------ #
    PAYMENT_CHECKOUT_URL = 'https://www.mypos.eu/vmp/checkout-test'
    PAYMENT_PRIVATE_KEY = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCf0TdcTuphb7X+Zwekt1XKEWZDczSGecfo6vQfqvraf5VPzcnJ
2Mc5J72HBm0u98EJHan+nle2WOZMVGItTa/2k1FRWwbt7iQ5dzDh5PEeZASg2UWe
hoR8L8MpNBqH6h7ZITwVTfRS4LsBvlEfT7Pzhm5YJKfM+CdzDM+L9WVEGwIDAQAB
AoGAYfKxwUtEbq8ulVrD3nnWhF+hk1k6KejdUq0dLYN29w8WjbCMKb9IaokmqWiQ
5iZGErYxh7G4BDP8AW/+M9HXM4oqm5SEkaxhbTlgks+E1s9dTpdFQvL76TvodqSy
l2E2BghVgLLgkdhRn9buaFzYta95JKfgyKGonNxsQA39PwECQQDKbG0Kp6KEkNgB
srCq3Cx2od5OfiPDG8g3RYZKx/O9dMy5CM160DwusVJpuywbpRhcWr3gkz0QgRMd
IRVwyxNbAkEAyh3sipmcgN7SD8xBG/MtBYPqWP1vxhSVYPfJzuPU3gS5MRJzQHBz
sVCLhTBY7hHSoqiqlqWYasi81JzBEwEuQQJBAKw9qGcZjyMH8JU5TDSGllr3jybx
FFMPj8TgJs346AB8ozqLL/ThvWPpxHttJbH8QAdNuyWdg6dIfVAa95h7Y+MCQEZg
jRDl1Bz7eWGO2c0Fq9OTz3IVLWpnmGwfW+HyaxizxFhV+FOj1GUVir9hylV7V0DU
QjIajyv/oeDWhFQ9wQECQCydhJ6NaNQOCZh+6QTrH3TC5MeBA1Yeipoe7+BhsLNr
cFG8s9sTxRnltcZl1dXaBSemvpNvBizn0Kzi8G3ZAgc=
-----END RSA PRIVATE KEY-----
'''
    PAYMENT_PUBLIC_CERTIFICATE = '''
-----BEGIN CERTIFICATE-----
MIIBsTCCARoCCQCCPjNttGNQWDANBgkqhkiG9w0BAQsFADAdMQswCQYDVQQGEwJC
RzEOMAwGA1UECgwFbXlQT1MwHhcNMTgxMDEyMDcwOTEzWhcNMjgxMDA5MDcwOTEz
WjAdMQswCQYDVQQGEwJCRzEOMAwGA1UECgwFbXlQT1MwgZ8wDQYJKoZIhvcNAQEB
BQADgY0AMIGJAoGBAML+VTmiY4yChoOTMZTXAIG/mk+xf/9mjwHxWzxtBJbNncNK
0OLI0VXYKW2GgVklGHHQjvew1hTFkEGjnCJ7f5CDnbgxevtyASDGst92a6xcAedE
adP0nFXhUz+cYYIgIcgfDcX3ZWeNEF5kscqy52kpD2O7nFNCV+85vS4duJBNAgMB
AAEwDQYJKoZIhvcNAQELBQADgYEACj0xb+tNYERJkL+p+zDcBsBK4RvknPlpk+YP
ephunG2dBGOmg/WKgoD1PLWD2bEfGgJxYBIg9r1wLYpDC1txhxV+2OBQS86KULh0
NEcr0qEY05mI4FlE+D/BpT/+WFyKkZug92rK0Flz71Xy/9mBXbQfm+YK6l9roRYd
J4sHeQc=
-----END CERTIFICATE-----
'''
    PAYMENT_WALLET_NUMBER = '61938166610'
    PAYMENT_STORE_ID = '000000000000010'
    PAYMENT_KEY_INDEX = 1


class TestingConfig(Config):
    TESTING = True

