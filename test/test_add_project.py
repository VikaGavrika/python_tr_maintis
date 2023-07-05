# -*- coding: utf-8 -*-
from model.project import Project
from data.projects import testdata
from fixtura.db import DbFixture
import pytest
import random
import string


db = DbFixture(host="127.0.0.1", name="bugtracker", user="root", password="")

@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project_UI(app, project):
    old_projects = app.project.get_project_list()
    app.project.create_new_project(project)
    new_projects = app.project.get_project_list()
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project_db(app, db, project, check_ui):
    old_projects = db.get_project_list()
    app.project.create_new_project(project)
    new_projects = db.get_project_list()
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    if check_ui:
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)



@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project_SOAP(app, project):
    #soap список старых проектов
    old_projects = app.soap.get_project_list()
    #добавляем проект через интерфейс
    app.project.create_new_project(project)
    # soap список новых проектов
    new_projects = app.soap.get_project_list()
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)