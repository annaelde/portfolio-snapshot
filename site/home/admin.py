"""
Creates admin panels for homepage content.
"""
from django.contrib import admin
from django import forms
from solo.admin import SingletonModelAdmin
from .models import SkillSet, Introduction

@admin.register(SkillSet)
class SkillAdmin(admin.ModelAdmin):
    """"
    Admin panel for skill sets
    """
    def get_form(self, request, obj=None, **kwargs):
        form = super(SkillAdmin, self).get_form(request, obj, **kwargs)
        for field in form.base_fields:
            form.base_fields.get(field).label_suffix = ''
        form.base_fields['skills'].widget = forms.Textarea(attrs={'rows': 3, 'cols': 40})
        return form


@admin.register(Introduction)
class IntroductionAdmin(SingletonModelAdmin):
    """ 
    Admin panel for front-page introduction
    """
    def get_form(self, request, obj=None, **kwargs):
        form = super(IntroductionAdmin, self).get_form(request, obj, **kwargs)
        for field in form.base_fields:
            form.base_fields.get(field).label_suffix = ''
        return form
