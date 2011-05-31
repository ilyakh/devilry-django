#!/usr/bin/env python

from optparse import OptionParser

from common import (setup_logging, load_devilry_plugins,
    add_settings_option, set_django_settings_module, add_quiet_opt,
    add_debug_opt)


p = OptionParser(
        usage = "%prog [options] <Subject short name> <Period short name>")
add_settings_option(p)
add_quiet_opt(p)
add_debug_opt(p)
(opt, args) = p.parse_args()
setup_logging(opt)

# Django must be imported after setting DJANGO_SETTINGS_MODULE
set_django_settings_module(opt)
from django.contrib.auth.models import User
from devilry.core.models import Subject

def exit_help():
    p.print_help()
    raise SystemExit()
setup_logging(opt)


tot_assignments = 0
tot_groups = 0
tot_deliveries = 0
all_students = set()
for subject in Subject.objects.all():
    print subject.short_name
    for period in subject.periods.all():
        print "    %s" % period.short_name
        assignments = period.assignments.all()
        period_deliveries = 0
        period_groups = 0
        for assignment in assignments:
            print "        %s" % assignment
            groups = assignment.assignmentgroups.all()
            tot_assignments += 1
            period_groups += len(groups)
            group_deliveries = 0
            student_count = 0
            for group in groups:
                group_deliveries += len(group.deliveries.all())
                for candidate in group.candidates.all():
                    all_students.add(candidate.student)
                    student_count += 1
            avg_students_per_group = float(student_count)/len(groups)
            group_deliveries += group_deliveries
            print "            Groups: %d" % len(groups)
            print "            Deliveries: %d" % group_deliveries
            print "            Avg number of students per group: %s" % avg_students_per_group
        tot_deliveries += period_deliveries
        tot_groups += period_groups
        print
        print "        Summary %s" % period
        print "            Assignments: %d" % len(assignments)
        print "            Groups: %d" % period_deliveries
        print "            Deliveries: %d" % period_deliveries
tot_students = len(all_students)

print """
Total assignments = %(tot_assignments)d
Total groups = %(tot_groups)d
Total deliveries: %(tot_deliveries)d
Total number of students = %(tot_students)d
""" % vars()
