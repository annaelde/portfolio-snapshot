"""
URLs for contact form. Used for processing when
AJAX is not available on client-side.
"""
from django.conf.urls import url
from .views import ContactView, SubmitView, ResultView

app_name = 'contact'

urlpatterns = [
    url(r'^$', ContactView.as_view(), name='contact'),
    url(r'^submit/$', SubmitView.as_view(), name='submit'),
    url(r'^success/$', ResultView.as_view(), {'status':302}, name='success'),
    url(r'^failure/$', ResultView.as_view(), {'status':400}, name='failure'),
]