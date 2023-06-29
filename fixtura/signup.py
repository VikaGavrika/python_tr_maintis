
import re

class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        #третьего поля капчи не будет, так как мы ее отключили
        #нажимаем сразу кнопку signup
        wd.find_element_by_css_selector('input[value="Signup"]').click()
        #делаем помощник по получению письма
        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        #из текста письма извлекаем ссылку
        url = self.extract_confirmation_url(mail)
        #проходим по ссылке
        wd.get(url)
        #завершаем регистрацию заполняем поля
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector('input[value="Update User"]').click()

    def extract_confirmation_url(self, text):
        return re.search("http://.*$", text, re.MULTILINE).group(0)
