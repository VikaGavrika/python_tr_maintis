
import poplib #чтоб получить почту
import email #для анализа текста
import time

class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        #тк почта может прийти не сразу, делаем несколько попыток, чтобы проитать сообщение
        for i in range(10):
            pop = poplib.POP3(self.app.config['james']['host']) #устанавливаем соед е с сервером
            pop.user(username)
            pop.pass_(password)
            #определяем кол-во писем
            num = pop.stat()[0] #возвращ инф о том что есть в почт ящике, первый элмент возвращ кортежа это кол-во писем
            if num > 0:
                #сравниваем тему письма с заданной в последнем приходящем письме. Находим текст письма, это второй элемент , то есть [1]
                for n in range(num):
                    msglines = pop.retr(n+1)[1]
                    msgtext = "\n".join(map(lambda x: x.decode('utf-8'), msglines))
                    msg = email.message_from_string(msgtext)
                    if msg.get("Subject") == subject:
                        pop.dele(n+1)
                        pop.quit()
                        return msg.get_payload()
            pop.quit()
            time.sleep(3)
        return None

