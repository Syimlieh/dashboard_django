from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

INV_CHOICES= [
    ('1', 'Check How Innovative my project is'),
    ('2', 'Check my answer against grant criteria'),
    ]

APP_CHOICES= [
    ('1', 'Mobile App'),
    ('2', 'Web App'),
    ('3', 'IOT'),
    ]

class WhatDoWant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    what_do_want = models.CharField(max_length=200, choices=INV_CHOICES, default='1')

class BriefOverview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_overview = models.CharField(max_length=500, null=True, blank=True)
    feature_1 = models.CharField(max_length=200, null=True, blank=True)
    feature_2 = models.CharField(max_length=200, null=True, blank=True)
    feature_3 = models.CharField(max_length=200, null=True, blank=True)
    feature_4 = models.CharField(max_length=200, null=True, blank=True)
    feature_5 = models.CharField(max_length=200, null=True, blank=True)
    competitor_1 = models.CharField(max_length=200, null=True, blank=True)
    competitor_2 = models.CharField(max_length=200, null=True, blank=True)
    competitor_3 = models.CharField(max_length=200, null=True, blank=True)
    app_choice = models.CharField(max_length=200, choices=APP_CHOICES, default='1')


class GrantApplyFor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grant_type = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class PREQualification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    grant = models.CharField(max_length=200, null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    current_score = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question1 = models.CharField(max_length=200, null=True, blank=True)
    question2 = models.CharField(max_length=200, null=True, blank=True)
    question3 = models.CharField(max_length=200, null=True, blank=True)
    question4 = models.CharField(max_length=200, null=True, blank=True)

class AssessorTips(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question1 = models.CharField(max_length=1000, null=True, blank=True)
    question2 = models.CharField(max_length=1000, null=True, blank=True)
