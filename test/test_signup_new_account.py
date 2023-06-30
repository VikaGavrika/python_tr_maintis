import random
import string

def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_signup_new_account(app):
    #создаем польз-я на почтовом сервере
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exists(username, password)
    #регистрируем поль-я на почтовом сервере
    app.signup.new_user(username, email, password)
    #проверка логина через интерфейс
    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.logout()

def test_signup_new_account_SOAP(app):
    #создаем польз-я на почтовом сервере
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exists(username, password)
    #регистрируем поль-я на почтовом сервере
    app.signup.new_user(username, email, password)
    #проверка логина через SOAP удаленный програмный интерфейс
    assert app.soap.can_login(username, password)