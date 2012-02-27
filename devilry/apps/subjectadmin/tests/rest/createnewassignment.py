from datetime import timedelta, datetime
from dingus import Dingus
from django.test import TestCase
import json
from django.contrib.auth.models import User

from devilry.apps.core.testhelper import TestHelper
from devilry.apps.subjectadmin.rest.createnewassignment import CreateNewAssignmentDao
from devilry.apps.subjectadmin.rest.createnewassignment import RestCreateNewAssignment
from devilry.apps.subjectadmin.rest.errors import PermissionDeniedError
from devilry.rest.testutils import dummy_urlreverse
from devilry.rest.testutils import isoformat_datetime
from devilry.rest.testutils import RestClient


class TestRestCreateNewAssignmentDao(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1:admin(p1admin)', 'p2'])
        self.testhelper.create_superuser("superuser")

    def test_create_assignment(self):
        dao = CreateNewAssignmentDao()
        publishing_time = self.testhelper.sub_p1.start_time + timedelta(days=1)
        assignment = dao._create_assignment(period_id=self.testhelper.sub_p1.id,
                                            short_name='a1', long_name='Assignment 1',
                                            publishing_time=publishing_time,
                                            delivery_types=0, anonymous=False)
        self.assertEquals(assignment.short_name, 'a1')
        self.assertEquals(assignment.long_name, 'Assignment 1')
        self.assertEquals(assignment.publishing_time, publishing_time)
        self.assertEquals(assignment.delivery_types, 0)
        self.assertEquals(assignment.anonymous, False)

    def _create_related_student(self, username, candidate_id=None, tags=None):
        user = self.testhelper.create_user(username)
        relatedstudent = self.testhelper.sub_p1.relatedstudent_set.create(user=user,
                                                                          candidate_id=candidate_id)
        if tags:
            relatedstudent.tags = tags
            relatedstudent.save()
        return relatedstudent

    def _create_related_examiner(self, username, tags=None):
        user = self.testhelper.create_user(username)
        relatedexaminer = self.testhelper.sub_p1.relatedexaminer_set.create(user=user)
        if tags:
            relatedexaminer.tags = tags
            relatedexaminer.save()
        return relatedexaminer

    def test_create_group_from_relatedstudent(self):
        dao = CreateNewAssignmentDao()
        self.testhelper.add_to_path('uni;sub.p1.a1')
        related_louie = self._create_related_student('louie')
        group = dao._create_group_from_relatedstudent(self.testhelper.sub_p1_a1, related_louie, [])
        self.assertEquals(group.candidates.all()[0].student.username, 'louie')
        self.assertEquals(group.candidates.all()[0].candidate_id, None)

        related_dewey = self._create_related_student('dewey', candidate_id='dew123',
                                                     tags='bb,aa')
        related_examiner1 = self._create_related_examiner('examiner1', tags='cc,dd')
        related_examiner2 = self._create_related_examiner('examiner2', tags='aa')
        group = dao._create_group_from_relatedstudent(self.testhelper.sub_p1_a1, related_dewey,
                                                      [related_examiner1, related_examiner2])
        self.assertEquals(group.candidates.all()[0].candidate_id, 'dew123')
        self.assertEquals(group.examiners.all().count(), 1)
        tags = group.tags.all().order_by('tag')
        self.assertEquals(len(tags), 2)
        self.assertEquals(tags[0].tag, 'aa')
        self.assertEquals(tags[1].tag, 'bb')

    def test_add_all_relatedstudents(self):
        self._create_related_student('louie')
        self._create_related_student('dewey', candidate_id='dew123')
        dao = CreateNewAssignmentDao()
        self.testhelper.add_to_path('uni;sub.p1.a1')

        self.assertEquals(self.testhelper.sub_p1_a1.assignmentgroups.count(), 0)
        deadline = self.testhelper.sub_p1_a1.publishing_time + timedelta(days=1)
        dao._add_all_relatedstudents(self.testhelper.sub_p1_a1, deadline, False)
        self.assertEquals(self.testhelper.sub_p1_a1.assignmentgroups.count(), 2)

        groups = list(self.testhelper.sub_p1_a1.assignmentgroups.all().order_by('candidates__student__username'))
        self.assertEquals(groups[0].candidates.all()[0].student.username, 'dewey')
        self.assertEquals(groups[0].candidates.all()[0].candidate_id, 'dew123')
        self.assertEquals(groups[1].candidates.all()[0].student.username, 'louie')
        self.assertEquals(groups[1].candidates.all()[0].candidate_id, None)

        self.assertEquals(groups[0].deadlines.all().count(), 1)
        self.assertEquals(groups[1].deadlines.all().count(), 1)
        self.assertEquals(groups[0].deadlines.all()[0].deadline, deadline)

    def test_add_all_relatedstudents_autosetup_examiners(self):
        self._create_related_student('louie', tags='bb,aa')
        self._create_related_examiner('examiner2', tags='aa,cc')
        dao = CreateNewAssignmentDao()
        self.testhelper.add_to_path('uni;sub.p1.a1')

        deadline = self.testhelper.sub_p1_a1.publishing_time + timedelta(days=1)
        dao._add_all_relatedstudents(self.testhelper.sub_p1_a1, deadline,
                                     autosetup_examiners=True)
        group = self.testhelper.sub_p1_a1.assignmentgroups.all()[0]
        self.assertEquals(group.examiners.all().count(), 1)

    def test_create_permissions(self):
        publishing_time = self.testhelper.sub_p1.start_time + timedelta(days=1)
        #first_deadline = self.testhelper.sub_p1.start_time + timedelta(days=2)
        kw = dict(period_id=self.testhelper.sub_p1.id,
                  short_name='a',
                  long_name='Aa', publishing_time=publishing_time,
                  delivery_types=0, anonymous=False,
                  add_all_relatedstudents=False, first_deadline=None,
                  autosetup_examiners=False)
        dao = CreateNewAssignmentDao()
        dao.create(self.testhelper.p1admin, **kw)
        nobody = self.testhelper.create_user('nobody')
        with self.assertRaises(PermissionDeniedError):
            dao.create(nobody, **kw)


class TestRestCreateNewAssignment(TestCase):
    def setUp(self):
        self.restapi = RestCreateNewAssignment(daocls=Dingus(), apiname='api',
                                               apiversion='1.0', user=None,
                                               url_reverse=dummy_urlreverse)

    def test_create(self):
        publishing_time = datetime(2010, 1, 1, 1, 1, 1)
        first_deadline = datetime(2011, 2, 2, 2, 2, 2)
        self.restapi.create(period_id=1001,
                            short_name='a', long_name='Aa',
                            publishing_time=isoformat_datetime(publishing_time),
                            delivery_types=0, anonymous=False,
                            add_all_relatedstudents=False,
                            first_deadline=isoformat_datetime(first_deadline),
                            autosetup_examiners=False)
        dingus = self.restapi.dao
        # Check the dingus to make sure all parameters was converted correctly
        self.assertEquals(1, len(dingus.calls('create', None, 1001, 'a', 'Aa',
                                              publishing_time, 0, False, False,
                                              first_deadline, False)))


class TestRestCreateNewAssignmentIntegration(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1:admin(p1admin)', 'p2'])
        self.client = RestClient()
        p1admin = User.objects.get(username='p1admin')
        self.client.login(username='p1admin', password='test')

    def test_create(self):
        publishing_time = self.testhelper.sub_p1.start_time + timedelta(days=1)
        first_deadline = self.testhelper.sub_p1.start_time + timedelta(days=2)
        data = dict(period_id=self.testhelper.sub_p1.id,
                    short_name='a', long_name='Aa',
                    publishing_time=isoformat_datetime(publishing_time),
                    delivery_types=0, anonymous=False,
                    add_all_relatedstudents=False,
                    first_deadline=isoformat_datetime(first_deadline),
                    autosetup_examiners=False)
        content, response = self.client.rest_create('/subjectadmin/rest/createnewassignment/',
                                                    **data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(content['success'], True)