from haystack import indexes
from haystack import site
from datetime import datetime

from devilry_search.base import BaseIndex
from .models import Node
from .models import Subject
from .models import Period
from .models import Assignment
from .models import AssignmentGroup
from .models import Examiner




class AdminsSearchIndex(BaseIndex):
    admin_ids = indexes.MultiValueField(model_attr='get_all_admin_ids')


class NodeIndex(AdminsSearchIndex):
    def index_queryset(self):
        qry = super(NodeIndex, self).index_queryset()
        qry = qry.prefetch_related('admins')
        return qry

site.register(Node, NodeIndex)


class SubjectIndex(AdminsSearchIndex):
    def index_queryset(self):
        qry = super(SubjectIndex, self).index_queryset()
        qry = qry.prefetch_related('admins')
        return qry

site.register(Subject, SubjectIndex)


class PeriodIndex(AdminsSearchIndex):
    start_time = indexes.DateTimeField(model_attr='start_time')
    end_time = indexes.DateTimeField(model_attr='end_time')

    def index_queryset(self):
        qry = super(PeriodIndex, self).index_queryset()
        qry = qry.select_related('parentnode')
        qry = qry.prefetch_related(
            'admins',
            'parentnode__admins')
        return qry

site.register(Period, PeriodIndex)


class AssignmentIndex(AdminsSearchIndex):
    publishing_time = indexes.DateTimeField(model_attr='publishing_time')
    is_active = indexes.BooleanField(model_attr='is_active')
    examiner_ids = indexes.MultiValueField()

    def prepare_examiner_ids(self, obj):
        return [examiner.user.id
                for examiner in Examiner.objects.filter(assignmentgroup__parentnode=obj.id)]

    def index_queryset(self):
        qry = super(AssignmentIndex, self).index_queryset()
        qry = qry.select_related(
            'parentnode'
            'parentnode__parentnode')
        qry = qry.prefetch_related(
            'admins',
            'parentnode__admins',
            'parentnode__parentnode__admins')
        return qry

site.register(Assignment, AssignmentIndex)


class AssignmentGroupIndex(AdminsSearchIndex):
    examiner_ids = indexes.MultiValueField()
    student_ids = indexes.MultiValueField()
    examiners = indexes.CharField(use_template=True)
    candidates = indexes.CharField(use_template=True)
    tags = indexes.CharField(use_template=True)
    is_active = indexes.BooleanField()
    is_published = indexes.BooleanField()

    def prepare_examiner_ids(self, obj):
        return [examiner.user.id for examiner in obj.examiners.all()]

    def prepare_student_ids(self, obj):
        return [candidate.student.id for candidate in obj.candidates.all()]

    def index_queryset(self):
        qry = super(AssignmentGroupIndex, self).index_queryset()
        qry = qry.select_related(
            'parentnode',  'parentnode__parentnode',
            'parentnode__parentnode__parentnode')
        qry = qry.prefetch_related(
            'tags',
            'parentnode__admins',
            'parentnode__parentnode__admins',
            'parentnode__parentnode__parentnode__admins',
            'examiners', 'examiners__user', 'examiners__user__devilryuserprofile',
            'candidates', 'candidates__student', 'candidates__student__devilryuserprofile')
        return qry

    def prepare_is_active(self, obj):
        return obj.parentnode.is_active()

    def prepare_is_published(self, obj):
        return obj.parentnode.publishing_time < datetime.now()



site.register(AssignmentGroup, AssignmentGroupIndex)