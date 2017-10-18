from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class ContactSitemap(Sitemap):
    changefreq = "never"
    priority = 0.2

    def items(self):
        return ['contact']
    
    def location(self, item):
        return reverse('contact:contact')
