from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from djangorestframework.views import View
from djangorestframework.resources import FormResource
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.response import Response
from django import forms

from devilry.apps.core.models import (AssignmentGroup,
                                      AssignmentGroupTag,
                                      Candidate,
                                      Examiner,
                                      Deadline)
from auth import IsAssignmentAdmin
from fields import ListOfDictField


class GroupDao(object):
    """
    Makes it convenient to work with everything related to an AssignmentGroup:

    - name
    - is_open
    - feedback
    - tags
    - deadlines
    - Candidates (students)
        - Candidate ID
        - Username
        - Full name
        - Email
    - Examiners
        - Username
        - Full name
        - Email
    """

    def _get_groups(self, assignmentid):
        """
        Get a list of group dictionaries.
        """
        fields = ('id', 'name', 'is_open', 'feedback__grade', 'feedback__points',
                  'feedback__is_passing_grade', 'feedback__save_timestamp',
                  'num_deliveries')
        qry = AssignmentGroup.objects.filter(parentnode=assignmentid)
        qry = qry.select_related('feedback')
        qry = qry.annotate(num_deliveries=Count('deadlines__deliveries'))
        return qry.values(*fields)

    def _prepare_group(self, group):
        """ Add the separate-query-aggreagated fields to the group dict. """
        group['tags'] = []
        group['students'] = []
        group['examiners'] = []
        group['deadlines'] = []
        return group

    def _convert_groupslist_to_groupsdict(self, groups):
        groupsdict = {}
        for group in groups:
            groupsdict[group['id']] = self._prepare_group(group)
        return groupsdict

    def _merge_with_groupsdict(self, groupsdict, listofdicts, targetkey, assignmentgroup_key='assignment_group_id'):
        for dct in listofdicts:
            group = groupsdict[dct[assignmentgroup_key]]
            del dct[assignmentgroup_key]
            group[targetkey].append(dct)

    def _get_candidates(self, assignmentid):
        fields = ('assignment_group_id', 'candidate_id',
                  'student__username', 'student__email',
                  'student__devilryuserprofile__full_name')
        return Candidate.objects.filter(assignment_group__parentnode=assignmentid).values(*fields)

    def _get_examiners(self, assignmentid):
        fields = ('assignmentgroup_id',
                  'user__username', 'user__email',
                  'user__devilryuserprofile__full_name')
        return Examiner.objects.filter(assignmentgroup__parentnode=assignmentid).values(*fields)

    def _get_tags(self, assignmentid):
        fields = ('assignment_group_id', 'tag')
        return AssignmentGroupTag.objects.filter(assignment_group__parentnode=assignmentid).values(*fields)

    def _get_deadlines(self, assignmentid):
        fields = ('assignment_group_id', 'deadline')
        return Deadline.objects.filter(assignment_group__parentnode=assignmentid).values(*fields)

    def _merge(self, groups, candidates, examiners, tags, deadlines):
        groupsdict = self._convert_groupslist_to_groupsdict(groups)
        self._merge_with_groupsdict(groupsdict, candidates, 'students')
        self._merge_with_groupsdict(groupsdict, examiners, 'examiners', assignmentgroup_key='assignmentgroup_id')
        self._merge_with_groupsdict(groupsdict, tags, 'tags')
        self._merge_with_groupsdict(groupsdict, deadlines, 'deadlines')
        return groupsdict.values()

    def list(self, assignmentid):
        """
        Returns a list of one dict for each group in the assignment with the
        given ``assignmentid``. The dict has the following keys:

        - name --- string
        - is_open --- boolean
        - feedback__grade --- string
        - feedback__points --- int
        - feedback__save_timestamp --- datetime
        - feedback__is_passing_grade --- boolean
        - students --- list of dicts with the following keys:
            - candidate_id --- string
            - student__username --- string
            - student__email --- string
            - student__devilryuserprofile__full_name --- string
        - examiners --- list of dicts with the following keys:
            - user__username --- string
            - user__devilryuserprofile__full_name --- string
            - user__email --- string
        - tags --- list of dicts with the following keys:
            - tag --- string
        - deadlines --- list of dicts with the following keys:
            - deadline --- datetime
        """
        groups = self._get_groups(assignmentid)
        candidates = self._get_candidates(assignmentid)
        examiners = self._get_examiners(assignmentid)
        tags = self._get_tags(assignmentid)
        deadlines = self._get_deadlines(assignmentid)
        groups = self._merge(groups, candidates, examiners, tags, deadlines)
        return groups


    def _setattr_if_not_none(self, obj, attrname, value):
        if value != None:
            setattr(obj, attrname, value)

    def _get_user(self, username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist, e:
            raise ValueError('User does not exist: {0}'.format(username))

    def _create_candidate_from_studentdict(self, group, studentdict):
        if not isinstance(studentdict, dict):
            raise ValueError('Each entry in the students list must be a dict. '
                             'Given type: {0}.'.format(type(studentdict)))
        try:
            username = studentdict['student__username']
        except KeyError, e:
            raise ValueError('A student dict must contain student__username. '
                             'Keys in the given dict: {0}.'.format(','.join(studentdict.keys())))
        else:
            candidate_id = studentdict.get('candidate_id')
            candidate = Candidate(assignment_group=group,
                                  student=self._get_user(username),
                                  candidate_id=candidate_id)
            candidate.save()
            return candidate

    def _create_from_singlekey_dict(self, modelcls, group, examinerdict, key,
                                    objectattr, getvalue=lambda v: v,
                                   assignmentgroupattr='assignment_group'):
        typename = modelcls.__class__.__name__
        if not isinstance(examinerdict, dict):
            raise ValueError('Each entry in the {typename} list must be a dict. '
                             'Given type: {giventypename}.'.format(typename=typename,
                                                                   giventypename=type(examinerdict)))
        try:
            value = examinerdict[key]
        except KeyError, e:
            raise ValueError('A {typename} dict must contain {key}. '
                             'Keys in the given dict: {keys}.'.format(typename=typename,
                                                                      key=key,
                                                                      keys=','.join(examinerdict.keys())))
        else:
            obj = modelcls()
            setattr(obj, assignmentgroupattr, group)
            setattr(obj, objectattr, getvalue(value))
            obj.save()
            return obj

    def _create_examiner_from_examinerdict(self, group, examinerdict):
        return self._create_from_singlekey_dict(Examiner, group, examinerdict,
                                                'user__username', 'user',
                                                assignmentgroupattr='assignmentgroup',
                                                getvalue=self._get_user)

    def _create_tag_from_tagdict(self, group, tagdict):
        return self._create_from_singlekey_dict(AssignmentGroupTag, group, tagdict, 'tag', 'tag')

    def _create_deadline_from_deadlinedict(self, group, deadlinedict):
        return self._create_from_singlekey_dict(Deadline, group, deadlinedict,
                                                'deadline', 'deadline')


    def create_noauth(self, assignmentid, name=None, is_open=None,
                      students=[], examiners=[], tags=[], deadlines=[]):
        group = AssignmentGroup(parentnode_id=assignmentid)
        self._setattr_if_not_none(group, 'name', name)
        self._setattr_if_not_none(group, 'is_open', is_open)
        group.save()
        for studentdict in students:
            self._create_candidate_from_studentdict(group, studentdict)
        for examinerdict in examiners:
            self._create_examiner_from_examinerdict(group, examinerdict)
        for tagdict in tags:
            self._create_tag_from_tagdict(group, tagdict)
        for deadlinedict in deadlines:
            self._create_deadline_from_deadlinedict(group, deadlinedict)
        return group

    def create(self, assignmentid, *args, **kwargs):
        return self.create_noauth(assignmentid, *args, **kwargs)




class TagsField(ListOfDictField):
    class Form(forms.Form):
        tag = forms.CharField()

class StudentsField(ListOfDictField):
    class Form(forms.Form):
        candidate_id = forms.CharField()
        student__username = forms.CharField()
        student__email = forms.CharField()
        student__devilryuserprofile__full_name = forms.CharField()

class DeadlinesField(ListOfDictField):
    class Form(forms.Form):
        deadline = forms.DateTimeField()

class ExaminersField(ListOfDictField):
    class Form(forms.Form):
        user__username = forms.CharField()
        user__email = forms.CharField()
        user__devilryuserprofile__full_name = forms.CharField()

class RestGroupRootForm(forms.Form):
    name = forms.CharField(required=False)
    is_open = forms.BooleanField(required=False)
    tags = TagsField(required=False)
    students = StudentsField(required=False)
    deadlines = DeadlinesField(required=False)
    examiners = ExaminersField(required=False)


class RestGroupRoot(View):
    resource = FormResource
    form = RestGroupRootForm
    permissions = (IsAuthenticated, IsAssignmentAdmin)
    def __init__(self):
        self.dao = GroupDao()

    def get(self, request, assignmentid):
        return self.dao.list(assignmentid)

    def post(self, request, assignmentid):
        group = self.dao.create(assignmentid, **self.CONTENT)
        return Response(201, dict(id=group.id))

#class RestGroup(View):
    #permissions = (IsAuthenticated, IsAssignmentAdmin)
    #def __init__(self, daocls=GroupDao):
        #self.dao = daocls()

    #def put(self, request, assignmentid):
        #return self.dao.list(assignmentid)