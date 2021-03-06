# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 20:58
from __future__ import unicode_literals
from django.db import migrations, transaction
from transfers.models import Student
from cps_migration.settings import BASE_DIR
import csv

### START CONFIG ###
data_dir = BASE_DIR + '/data/processed/'
transfer_filenames = [data_dir + x for x in 
        ['18-073-belsha-follow_up_doc_2009_to_2017__Year_After_CPS.csv', 
         '18-073-belsha-follow_up_doc_2009_to_2017__CPS_Enrollment.csv']
        ]
### END CONFIG ###


@transaction.atomic
def load_students(apps,schema_editor):
    print('loading students')
    for filename in transfer_filenames:
        transfer_csv = csv.DictReader(open(filename))    
        for row in transfer_csv:
            student, created = Student.objects.get_or_create(student_id=row['Student ID'])
            if created:
                student.save()


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0001_initial'),
    ]

    operations = [
            migrations.RunPython(load_students),
    ]
