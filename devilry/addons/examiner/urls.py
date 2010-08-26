from django.conf.urls.defaults import *



urlpatterns = patterns('devilry.addons.examiner',
    url(r'^choose-assignment$',
        'views.choose_assignment',
        name='devilry-examiner-choose_assignment'),
    url(r'^show-assignmentgroup/(?P<assignmentgroup_id>\d+)$',
        'views.show_assignmentgroup',
        name='devilry-examiner-show_assignmentgroup'),
    url(r'^delete-deadline/(?P<assignmentgroup_id>\d+)/(?P<deadline_id>\d+)$',
        'views.delete_deadline',
        name='devilry-examiner-delete_deadline'),
    url(r'^correct-delivery/(?P<delivery_id>\d+)$',
        'views.correct_delivery',
        name='devilry-examiner-correct_delivery'),
    url(r'^list_assignmentgroups/(?P<assignment_id>\d+)$',
        'views.list_assignmentgroups',
        name='devilry-examiner-list_assignmentgroups'),
    url(r'^assignmentgroup_filtertable_json$',
        'views.assignmentgroup_filtertable_json',
        name='devilry-examiner-assignmentgroup_filtertable_json'),
)
