from django.utils.translation import ugettext as _


def make_settings_summary_subset(status):
    print dir(status)
    settings = status.devilry_qualifiesforexam_approved_subsetpluginsetting
    out = [_(u'Selected assignments'), u': ']
    longnames = [selected.assignment.long_name for selected in settings.selectedassignment_set.all()]
    out.append(', '.join(longnames))
    return ''.join(out)
