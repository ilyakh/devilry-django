from devilry.apps.core.testhelper import TestHelper

from .base import SubjectAdminSeleniumTestCase



class RelatedUsersUITestMixin(object):
    def find_element(self, cssselector):
        return self.selenium.find_element_by_css_selector('.devilry_subjectadmin_relatedusers {0}'.format(cssselector))
    def find_elements(self, cssselector):
        return self.selenium.find_elements_by_css_selector('.devilry_subjectadmin_relatedusers {0}'.format(cssselector))

    def waitForGridRowCount(self, count):
        self.waitFor(self.selenium, lambda s: len(self.find_gridrows()) == count)

    def find_gridrows(self):
        return self.find_elements('.devilry_subjectadmin_relatedusergrid .x-grid-row')

    def get_row_by_username(self, username):
        for row in self.find_gridrows():
            matches = row.find_elements_by_css_selector('.relateduser_username_{username}'.format(username=username))
            if len(matches) > 0:
                return row

    def select_row_by_username(self, username):
        self.get_row_by_username(username).click()

    def get_row_data(self, row):
        result = {}
        result['full_name'] = row.find_element_by_css_selector('.meta_cell .full_name').text.strip()
        result['username'] = row.find_element_by_css_selector('.meta_cell .username').text.strip()
        result['tags'] = row.find_element_by_css_selector('.tags_cell').text.strip()
        candidate_id_elements = row.find_elements_by_css_selector('.meta_cell .candidate_id')
        if len(candidate_id_elements) == 1:
            result['candidate_id'] = candidate_id_elements[0].text.strip()
        return result


    def ui_add_related_user(self, username):
        self.waitForCssSelector('.add_related_user_button')
        addbutton = self.find_element('.add_related_user_button')
        usersearchfield = self.find_element('.devilry_subjectadmin_selectrelateduserpanel input[type=text]')
        addbutton.click()
        self.waitForDisplayed(usersearchfield)
        usersearchfield.send_keys(username)
        match = self.waitForAndFindElementByCssSelector('.autocompleteuserwidget_matchlist .matchlistitem_{0}'.format(username))
        match.click()
        self.waitForNotDisplayed(usersearchfield)


class TestRelatedStudentsUI(SubjectAdminSeleniumTestCase, RelatedUsersUITestMixin):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1:admin(p1admin)'])
        self.period = self.testhelper.sub_p1

    def _browseToManageStudentsAs(self, username, period_id):
        path = '/period/{0}/@@related-students'.format(period_id)
        self.loginTo(username, path)
        self.waitForCssSelector('.devilry_subjectadmin_relatedstudents')


    def _add_relatedstudent(self, username, full_name=None, tags='', candidate_id=None):
        user = self.testhelper.create_user(username, fullname=full_name)
        self.period.relatedstudent_set.create(user=user,
                                              tags=tags,
                                              candidate_id=candidate_id)

    def test_render(self):
        self._add_relatedstudent('student1', full_name='Student One',
                                 tags='a,b',
                                 candidate_id='SEC-RET')
        self._add_relatedstudent('student2')
        self._add_relatedstudent('student3', full_name='Student Three')
        self._browseToManageStudentsAs('p1admin', self.period.id)

        self.waitForCssSelector('.devilry_subjectadmin_selectrelateduserpanel')
        self.waitForGridRowCount(3)
        self.assertEquals(self.get_row_data(self.get_row_by_username('student1')),
                          {'full_name': 'Student One',
                           'username': 'student1',
                           'tags': 'a,b',
                           'candidate_id': 'SEC-RET'})
        self.assertEquals(self.get_row_data(self.get_row_by_username('student2')),
                          {'full_name': 'Full name missing',
                           'username': 'student2',
                           'tags': ''})
        self.assertEquals(self.get_row_data(self.get_row_by_username('student3')),
                          {'full_name': 'Student Three',
                           'username': 'student3',
                           'tags': ''})

    def test_invalid_period_id(self):
        self._browseToManageStudentsAs('p1admin', 1000000)
        # Should get one error for Period, and one for relatedusers
        self.waitFor(self.selenium, lambda s: len(s.find_elements_by_css_selector('.devilry_extjsextras_alertmessage')) == 2)
        for message in self.find_elements('.devilry_extjsextras_alertmessage'):
            self.assertIn('403', message.text.strip())

    def test_add_student(self):
        self._browseToManageStudentsAs('p1admin', self.period.id)
        self.waitForCssSelector('.devilry_subjectadmin_selectrelateduserpanel')
        self.testhelper.create_user('student1')
        self.ui_add_related_user('student1')
        self.waitForGridRowCount(1)
        # TODO: Wait for success message, and test the database.
