from datetime import date, timedelta
from devilry.apps.core.testhelper import TestHelper
from devilry.apps.core.models import Assignment, AssignmentGroup

from .base import SubjectAdminSeleniumTestCase


class TestCreateNewAssignment(SubjectAdminSeleniumTestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.create_superuser('grandma')
        self.login('grandma')
        self.tomorrow = date.today() + timedelta(days=1)

        self.testhelper.add(nodes='uni',
                            subjects=['duck1100'],
                            periods=['2012h:begins(-1)'])
        self.period_id = self.testhelper.duck1100_2012h.id

    def test_form_render(self):
        self.browseTo('/@@create-new-assignment/{0}'.format(self.period_id))
        self.waitForCssSelector('.createnewassignmentform')

        self.assertTrue('Create new assignment' in self.selenium.page_source)

        self.assertTrue('Long name' in self.selenium.page_source)
        self.assertTrue('Example of assignment long name' in self.selenium.page_source)
        self.assertTrue('Choose a descriptive name for your assignment' in self.selenium.page_source)

        self.assertTrue('Choose a short name with at most 20 letters for your assignment' in self.selenium.page_source)
        self.assertTrue('Short name' in self.selenium.page_source)
        self.assertTrue('How do students add deliveries?' in self.selenium.page_source)

    def test_invalid_period(self):
        self.browseTo('/@@create-new-assignment/1001')
        self.waitForCssSelector('.createnewassignmentform')
        self.assertTrue('Period 1001 is not an active period.' in self.selenium.page_source)

    def test_form_render_advanced_fieldset(self):
        self.browseTo('/@@create-new-assignment/{0}'.format(self.period_id))
        self.waitForCssSelector('.createnewassignmentform')
        self.assertTrue('Advanced options' in self.selenium.page_source)

        self.assertFalse('Anonymous?' in self.selenium.page_source)
        self.assertFalse('Publishing time' in self.selenium.page_source)
        self.assertFalse('Add all students to this assignment?' in self.selenium.page_source)
        self.assertFalse('Automatically setup examiners?' in self.selenium.page_source)

        fieldsetbutton = self.selenium.find_element_by_css_selector('.advanced_options_fieldset legend .x-tool img')
        fieldsetbutton.click()

        self.assertTrue('Anonymous?' in self.selenium.page_source)
        self.assertTrue('If an assignment is anonymous, examiners see a candidate-id instead of a username' in self.selenium.page_source)
        self.assertTrue('Publishing time' in self.selenium.page_source)
        self.assertTrue('Add all students to this assignment?' in self.selenium.page_source)
        self.assertTrue('Automatically setup examiners?' in self.selenium.page_source)


    def _set_value(self, fieldname, value):
        field = self.selenium.find_element_by_css_selector('input[name={0}]'.format(fieldname))
        field.send_keys(value)

    def _set_datetime_value(self, fieldclass, field, value):
        field = self.selenium.find_element_by_css_selector('.{fieldclass} .datetimefield_{field} input[type=text]'.format(fieldclass=fieldclass,
                                                                                                                          field=field))
        field.send_keys(value)

    def _set_first_deadline(self, date, time):
        self._set_datetime_value('first_deadline', 'date', date)
        self._set_datetime_value('first_deadline', 'time', time)

    def test_form_createbutton(self):
        self.browseTo('/@@create-new-assignment/{0}'.format(self.period_id))
        self.waitForCssSelector('.createnewassignmentform')

        createbutton = self.selenium.find_element_by_css_selector('.createbutton button')
        self.assertFalse(createbutton.is_enabled())

        # Make sure the create button is clickable after both short and long names are entered.
        self._set_value('long_name', 'Test')
        self.assertFalse(createbutton.is_enabled())

        self._set_value('short_name', 'test')
        self.waitForEnabled(createbutton)

    def _click_createbutton(self):
        createbutton = self.selenium.find_element_by_css_selector('.createbutton button')
        self.waitForEnabled(createbutton)
        createbutton.click()

    def test_duplicate(self):
        self.testhelper.add_to_path('uni;duck1100.2012h.a1')
        self.browseTo('/@@create-new-assignment/{0}'.format(self.period_id))
        self.waitForCssSelector('.createnewassignmentform')
        self._set_value('long_name', 'A1')
        self._set_value('short_name', 'a1')
        self._set_first_deadline(self.tomorrow.isoformat(), '15:00')
        self._click_createbutton()
        self.waitForCssSelector('.alertmessagelist')
        self.assertTrue('Assignment with this Short name and Period already exists' in self.selenium.page_source)

    def test_success(self):
        self.browseTo('/@@create-new-assignment/{0}'.format(self.period_id))
        self.waitForCssSelector('.createnewassignmentform')

        self._set_value('long_name', 'Test')
        self._set_value('short_name', 'sometest')
        self._set_first_deadline(self.tomorrow.isoformat(), '15:00')
        self._click_createbutton()

        self.waitForCssSelector('.createnewassignment-successpanel')
        links = self.selenium.find_elements_by_css_selector('.actionlist a')
        self.assertEquals(len(links), 2)
        self.assertEquals(links[0].get_attribute('href'), 'http://localhost:8081/devilry_subjectadmin/#/duck1100/2012h/sometest/')
        self.assertEquals(links[1].get_attribute('href'), u'http://localhost:8081/devilry_subjectadmin/#/@@create-new-assignment/1')

        created = Assignment.objects.get(parentnode__id=self.period_id, short_name='sometest')
        self.assertEquals(created.long_name, 'Test')
        return created


    def _create_related_student(self, username, candidate_id=None, tags=None):
        user = self.testhelper.create_user(username)
        relatedstudent = self.testhelper.duck1100_2012h.relatedstudent_set.create(user=user,
                                                                          candidate_id=candidate_id)
        if tags:
            relatedstudent.tags = tags
            relatedstudent.save()
        return relatedstudent

    def _create_related_examiner(self, username, tags=None):
        user = self.testhelper.create_user(username)
        relatedexaminer = self.testhelper.duck1100_2012h.relatedexaminer_set.create(user=user)
        if tags:
            relatedexaminer.tags = tags
            relatedexaminer.save()
        return relatedexaminer

    def test_create_with_related(self):
        self._create_related_student('student0', tags=['group1'])
        self._create_related_student('student1', tags=['group1'])
        self._create_related_student('student2', tags=['group1'])
        self._create_related_student('student3', tags=['group2'])
        self._create_related_examiner('examiner0', tags=['group1'])
        created = self.test_success()
        self.assertEquals(created.assignmentgroups.all().count(), 4)
        student0group = AssignmentGroup.where_is_candidate(self.testhelper.student0).get(parentnode=created.id)
        self.assertEquals(student0group.examiners.all()[0].user, self.testhelper.examiner0)
        self.assertEquals(student0group.deadlines.count(), 1)
        self.assertEquals(student0group.deadlines.all()[0].deadline.date(), self.tomorrow)
        self.assertEquals(student0group.deadlines.all()[0].deadline.time().hour, 15)
        self.assertEquals(student0group.deadlines.all()[0].deadline.time().minute, 0)

    def test_success_direct(self):
        self.browseTo('/@@create-new-assignment/@@success')
        self.waitForCssSelector('.x-message-box')
        self.assertTrue('This page is only available after creating a new assignment.' in self.selenium.page_source)