
from model.project import Project


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    project_cache = None

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_xpath("//a[contains(text(),'Manage')]").click()
            wd.find_element_by_xpath("//a[contains(text(),'Manage Projects')]").click()

    def create_new_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        # init project creation
        wd.find_element_by_css_selector("td.form-title > form > input.button-small").click()
        # fill project form
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys("%s" % project.name)
        # submit project creation
        wd.find_element_by_css_selector("input.button").click()
        self.project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_projects_page()
            self.project_cache = []
            for element in wd.find_elements_by_xpath(
                    "//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]"):
                project_name = element.text
                string_id = element.get_attribute("href")
                id = string_id[string_id.find('project_id=') + len('project_id='):]
                self.project_cache.append(Project(name=project_name, id=id))
        return list(self.project_cache)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.select_project_by_id(id)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.project_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href, 'manage_proj_edit_page.php?project_id=%s')]" % id).click()
















