

from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password): #проверка того,что пользователь может войти в систему
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_link(self):
        return Client(self.app.config['web']['baseUrl'] + "api/soap/mantisconnect.php?wsdl")

    def get_project_list(self):
        username = self.app.config['web']['username']
        password = self.app.config['web']['password']
        client = self.get_link()
        try:
            #Get the list of projects that are accessible to the logged in user
            #Получить список проектов, доступных для вошедшего в систему пользователя.
            project_data = client.service.mc_projects_get_user_accessible(username, password)
            projects = []
            for element in project_data:
                id = element.id
                name = element.name
                projects.append(Project(id=id, name=name))
            return list(projects)
        except WebFault:
            return False

