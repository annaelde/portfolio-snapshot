"""
Views to handle processing for the contact form.
"""
import json
import urllib

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .forms import ContactForm


class ContactView(CreateView):
    """
    Handles AJAX submissions for the contact form.
    """
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        """
        Add public key to the context.
        """
        context = super(ContactView, self).get_context_data(**kwargs)
        context['GOOGLE_RECAPTCHA_PUBLIC_KEY'] = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
        return context

    def post(self, request, *args, **kwargs):
        """
        Processes the form and sends a JSON response back.
        """
        form = ContactForm(request.POST)

        if form.is_valid():
            # Check reCAPTCHA
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # If reCAPTCHA valid, submit
            if result['success']:
                form.clean()
                message = '{0} submitted a message.\n\n{2}\n\nResponse Email: {1}'
                message = message.format(*form.cleaned_data.values())
                email = EmailMessage('Contact Form | Anna Elde Codes', message, to=[settings.PERSONAL_EMAIL])
                email.send()
                return JsonResponse({'response': 'Thanks for your submission!'}, status=201)
            # Else, return a custom error message
            else:
                return JsonResponse({'response': 'Did you fill out reCAPTCHA? Please try submitting the form again.'}, status=400)
        else:
            return JsonResponse({'response': 'Your form submission is not valid. Please make sure you filled out the form correctly.'}, status=400)


class SubmitView(CreateView):
    """
    Handles HTML-only submissions for the contact form.
    """
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        """
        Redirects improper GET requests to the failure page.
        """
        return HttpResponseRedirect(reverse('contact:failure'))

    def post(self, request, *args, **kwargs):
        """
        Processes form and determines which page to redirect to.
        """
        form = ContactForm(request.POST)
        if form.is_valid():
            # Check reCAPTCHA
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # If reCAPTCHA valid, submit
            if result['success']:
                form.clean()
                message = '{0} submitted a message.\n\n{2}\n\nResponse Email: {1}'
                message = message.format(*form.cleaned_data.values())
                email = EmailMessage('Contact Form | Anna Elde Codes', message, to=[settings.PERSONAL_EMAIL])
                email.send()
                return HttpResponseRedirect(reverse('contact:success'))

        return HttpResponseRedirect(reverse('contact:failure'))


class ResultView(TemplateView):
    """
    Redirect page for HTML-only submissions.
    """
    template_name = 'contact/result.html'

    def get_context_data(self, **kwargs):
        """
        Adds correct context data based on URL kwargs
        """
        context = super(ResultView, self).get_context_data(**kwargs)
        if kwargs.get('status', None) == 302:
            context['title'] = 'Submission Succeeded'
            context['result'] = 'Thanks for leaving me a message! I\'ll try to respond soon.'
        else:
            context['title'] = 'Submission Failed'
            context['result'] = 'Oops, something went wrong! Please try submitting the form again.'
        return context
