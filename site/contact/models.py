"""
Defines message model for use in contact form.
"""
from django.db import models
from django.template.defaultfilters import date

class Message(models.Model):
    name = models.CharField(max_length=64, default='')
    email = models.CharField(max_length=64, default='')
    content = models.CharField(max_length=256, default='')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' | ' + date(self.date, "m.d.y @ fA") 