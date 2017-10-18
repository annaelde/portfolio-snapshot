"""
URLs for portfolio projects.
"""
from django.conf.urls import url
from portfolio.views import ProjectListView, ProjectDetailView

app_name = 'portfolio'

urlpatterns = [
    # ex: /projects/
    url(r'^$', ProjectListView.as_view(), name='project_list'),
    # ex: /projects/slug/
    url(r'^(?P<slug>[-\w\d]+)/$', ProjectDetailView.as_view(), name='project_detail')
]