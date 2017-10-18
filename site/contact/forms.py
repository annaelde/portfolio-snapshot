"""
Defines contact form.
"""
from django import forms
from .models import Message


class ContactForm(forms.ModelForm):
    error_css_class = "error"
    email = forms.EmailField(max_length=64, required=True)
    content = forms.CharField(max_length=256,widget=forms.Textarea, required=True)
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Message
        fields = ['name','email','content']
