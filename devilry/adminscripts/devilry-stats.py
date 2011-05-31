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
    print
    print subject.short_name
    print '-----------------------'
    for period in subject.periods.all():
        print "    %s" % period.short_name
        assignments = period.assignments.all()
        period_deliveries = 0
        period_groups = 0
        period_students = set()
        for assignment in assignments:
            groups = assignment.assignmentgroups.all()
            if len(groups) > 0:
                print "        %s" % assignment
                tot_assignments += 1
                group_deliveries = 0
                student_count = 0
                assignment_groupcount = 0
                for group in groups:
                    candidates = group.candidates.all()
                    if len(candidates) > 0:
                        group_deliveries += len(group.deliveries.all())
                        assignment_groupcount += 1
                        for candidate in candidates:
                            period_students.add(candidate.student)
                            student_count += 1
                if(len(groups)) > 0:
                    avg_students_per_group = float(student_count)/assignment_groupcount
                else:
                    avg_students_per_group = 0
                period_deliveries += group_deliveries
                period_groups += assignment_groupcount
                print "            Groups: %d" % assignment_groupcount
                print "            Deliveries: %d" % group_deliveries
                print "            Avg number of students per group: %s" % avg_students_per_group
        tot_deliveries += period_deliveries
        tot_groups += period_groups
        all_students.update(period_students)
        print
        print "        Summary %s" % period
        print "            Assignments: %d" % len(assignments)
        print "            Students: %d" % len(period_students)
        print "            Groups: %d" % period_groups
        print "            Deliveries: %d" % period_deliveries
tot_students = len(all_students)

print """
Total Assignments = %(tot_assignments)d
Total Students = %(tot_students)d
Total Groups = %(tot_groups)d
Total Deliveries: %(tot_deliveries)d
""" % vars()
