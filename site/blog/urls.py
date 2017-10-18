"""
URLs for the blog, including list view and detail view.
"""
from django.conf.urls import url
from .views import PostListView, PostDetailView

app_name = 'blog'
urlpatterns = [
    # ex: /blog/
    url(r'^$', PostListView.as_view(), name='post_list'),
    # ex: /blog/slug/
    url(r'^(?P<slug>[-\w\d]+)/$', PostDetailView.as_view(), name='post_detail')
]