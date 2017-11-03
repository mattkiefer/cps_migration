# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from geos.models import CommArea

class Student(models.Model):
    student_id = models.CharField(max_length=10,primary_key=True)

class District(models.Model):
    name = models.CharField(max_length=50)


class School(models.Model):
    county = models.CharField(null=True,max_length=30)
    cat = models.IntegerField(null=True)
    rcdts = models.CharField(null=True,max_length=20)
    name = models.CharField(null=True,max_length=100)

    k12 = models.IntegerField(null=True)
    housed = models.IntegerField(null=True)
    low_income = models.IntegerField(null=True)

    male = models.IntegerField(null=True)
    female = models.IntegerField(null=True)
    hispanic = models.IntegerField(null=True)
    am_ind = models.IntegerField(null=True)
    asian = models.IntegerField(null=True)
    black = models.IntegerField(null=True)
    opi = models.IntegerField(null=True)
    white = models.IntegerField(null=True)
    multiple_races = models.IntegerField(null=True)

    pre_k = models.IntegerField(null=True)
    kind = models.IntegerField(null=True)
    first = models.IntegerField(null=True)
    second = models.IntegerField(null=True)
    third = models.IntegerField(null=True)
    fourth = models.IntegerField(null=True)
    fifth = models.IntegerField(null=True)
    sixth = models.IntegerField(null=True)
    seventh = models.IntegerField(null=True)
    eighth = models.IntegerField(null=True)
    ninth = models.IntegerField(null=True)
    tenth = models.IntegerField(null=True)
    eleventh = models.IntegerField(null=True)
    twelfth = models.IntegerField(null=True)

    administrator = models.CharField(null=True,max_length=100)
    address = models.CharField(null=True,max_length=100)
    city = models.CharField(null=True,max_length=50)
    zip_code = models.CharField(null=True,max_length=12)
    phone = models.CharField(null=True,max_length=15)
    grades_served = models.CharField(null=True,max_length=20)

    rec_type = models.CharField(null=True,max_length=40)
    
    st_rep = models.IntegerField(null=True)
    st_sen = models.IntegerField(null=True)
    fed_cong = models.IntegerField(null=True)
    cat = models.CharField(null=True,max_length=5)
    nces_id = models.CharField(null=True,max_length=20)

    cps_id = models.IntegerField(null=True)
    comm_area_name = models.CharField(null=True,max_length=40)
    comm_area = models.ForeignKey(CommArea,null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    cps_closed = models.NullBooleanField()
    attendance_type = models.CharField(null=True,max_length=40)

    dist_name = models.CharField(null=True,max_length=50)
    district = models.ForeignKey(District,null=True)


class Transfer(models.Model):
    student_id_no = models.IntegerField(null=True)
    student = models.ForeignKey(Student,null=True)
    school_year = models.IntegerField(null=True)
    fte = models.FloatField(null=True)
    from_home_school = models.ForeignKey(School,related_name='from_home_school',null=True)
    from_home_rcdts = models.CharField(null=True,max_length=20)
    from_serving_school = models.ForeignKey(School,related_name='from_serving_school',null=True)
    from_serving_rcdts = models.CharField(null=True,max_length=20)
    to_home_school = models.ForeignKey(School,related_name='to_home_school',null=True)
    to_home_rcdts = models.CharField(null=True,max_length=20)
    to_serving_school = models.ForeignKey(School,related_name='to_serving_school',null=True)
    to_serving_rcdts = models.CharField(null=True,max_length=20)
    enrollment_date = models.DateField(null=True)
    exit_date = models.DateField(null=True)
    exit_code = models.IntegerField(null=True)
    exit_desc = models.CharField(null=True,max_length=200)
