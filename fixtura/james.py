
from telnetlib import Telnet


class JamesHelper:
    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, username, password):
        james_config = self.app.config["james"]
        session = JamesHelper.Session(
            james_config["host"], james_config["port"], james_config["username"], james_config["password"])
        if session.is_users_registered(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

    class Session:

         def __init__(self, host, port, username, password): #берем из таргет.джейсон. Юзернэйм это логин и пасворд это пароль для доступа к почтову серверу, а не логин и пароль пользователя которого собираемся создать
             self.telnet = Telnet(host, port, 5) #таймаут 5 сек если сервер не отвечает #соединение установили
             self.read_until("Login id:") #выполняем вход #читаем до тех пор пока не будет Логин #таймаут 5 сек
             self.write(username + "\n") #вводим юзернэйм и перевод строки
             self.read_until("Password:") #читаем до тех пор пока не появляется пароль и ожидаем 5 сек
             self.write(password + "\n") #вводим пасворд и перевод строки
             self.read_until("Welcome root. HELP for a list of commands") #читаем до тех пор пока не появляется сообщ об успеш входе и ожидаем 5 сек

         def read_until(self, text): #функция перекодировки в тип данных байт
             self.telnet.read_until(text.encode("ascii"), 5)

         def write(self, text):
            self.telnet.write(text.encode("ascii"))

         def is_users_registered(self, username): #проверка сущ-я польз-ля
             self.write("verify %s\n" % username)
             res = self.telnet.expect([b"exist", b"does not exist"])
             return res[0] == 0

         def create_user(self, username, password): #создание польз-я
             self.write("adduser %s %s\n" % (username, password))
             self.read_until("User %s added" % username)

         def reset_password(self, username, password): #смена пароля
             self.write("setpassword %s %s\n" % (username, password))
             self.read_until("Password for %s reset" % username)

         def quit(self):
             self.write("quit\n")
