"""
check the db counts
against raw source files, make sure
totals match up right
"""
# TODO: this isn't functional. 
# next time, think ahead about how to store paths 
# of converted files as configs for sanity checks

import csv
from transfers.models import Student, School, Transfer
from geos.models import CommArea
#from convert import transfers_in_path

transfers = [x for x in Transfer.objects.all()]
students = [x for x in Student.objects.all()]
schools = [x for x in School.objects.all()]
commareas = [x for x in CommArea.objects.all()]

def check_transfer_counts():
    complete_transfers = [x for x in transfers if x.to_home_school and \
            x.to_serving_school and x.from_home_school and \
            x.from_serving_school]
    print len(complete_transfers)
    return complete_transfers

def check_student_counts():
    pass

def check_school_counts():
    pass


def check_comm_area_counts():
    pass



def check_counts():
    check_transfer_counts()
