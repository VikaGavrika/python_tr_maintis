from model.project import Project
import random
from fixtura.db import DbFixture


db = DbFixture(host="127.0.0.1", name="bugtracker", user="root", password="")


def test_delete_project_db(app, db, check_ui):
    if len(db.get_project_list()) == 0:
        app.project.create_new_project(Project(name="1"))
    old_projects = db.get_project_list()
    #поиск нужной проекта и удаление ее по идентификатору
    project = random.choice(old_projects)
    #обращ-ся к функции и в кач параметра передаем индентифик проекта
    app.project.delete_project_by_id(project.id)
    new_projects = db.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    #удаление старого элемента из списка
    old_projects.remove(project)
    assert old_projects == new_projects
    if check_ui:
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)

def test_delete_project_Ui(app):
    if len(app.project.get_project_list()) == 0:
        app.project.create_new_project(Project(name="1111111111111"))
    old_projects = app.project.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.project.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects

def test_delete_project_SOAP(app):
    # будем получать список проектов пользователя administrator с паролем root (как и выше добавляли проекты под этим польз-ем)
    web_config = app.config['web']
    username = web_config['username']
    password = web_config['password']
    if len(app.soap.get_project_list(username, password)) == 0:
        app.project.create_new_project(Project(name="11111111111"))
    # soap список старых проектов
    old_projects = app.soap.get_project_list(username, password)
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    # soap список новых проектов
    new_projects = app.soap.get_project_list(username, password)
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects