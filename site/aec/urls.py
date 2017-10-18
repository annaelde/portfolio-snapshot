from django.conf import settings
from django.conf.urls import (handler400, handler403, handler404, handler500,
                              include, url)
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from .sitemaps import sitemaps

urlpatterns = [
    url(r'^$', include('home.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^projects/', include('portfolio.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^sitemap\.xml$', sitemap, {
        'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Admin settings
admin.site.site_header = 'anna.elde.codes'
admin.site.site_title = 'anna.elde.codes'

# Change to callable for Django 2.0
handler400 = 'aec.views.bad_request'
handler403 = 'aec.views.permission_denied'
handler404 = 'aec.views.page_not_found'
handler500 = 'aec.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
