# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Criminal(models.Model):

    SSN = models.CharField(max_length=9, primary_key=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=('F', 'M'))
    height_in_ft = models.FloatField()
    weight_in_kg = models.IntegerField()
    races = ('African American',
             'White',
             'Arab',
             'Asian',
             'Black',
             'Romanian',
             'Hispanic and Latino American',
             'British',
             'Cuban',
             'Korean',
             'English',
             'British',
             'Somalian',
             'Indian',
             'Indian American',
             'Chinese American',
             'Chinese'
             'Japanese')
    ethnicity = models.CharField(max_length=30, choices=races)
    hair_colour = models.CharField(max_length=20)
    dist_mark = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=('In prison',
                                                      'In Jail',
                                                      'Bail',
                                                      'Acquitted',
                                                      'Suspect',
                                                      'On the run'))
    occupation = models.CharField(max_length=30)


class Detective(models.Model):

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact_no = models.IntegerField(unique=True)


class Dependent(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    relationship = models.CharField(max_length=20)
    contact_no = models.IntegerField(unique=True)


class Crime(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=30)


class Case(models.Model):
    id = models.IntegerField(primary_key=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    description = models.TextField(max_length=70)


class AssignedTo(models.Model):
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE)
    det_id = models.ForeignKey(Detective, on_delete=models.CASCADE)


class DependsOn(models.Model):
    criminal_ssn = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    dep_f_name = models.CharField(max_length=20)
    dep_l_name = models.CharField(max_length=20)


class ConnectedTo(models.Model):
    ssn = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE)
