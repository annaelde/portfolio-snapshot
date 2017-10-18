from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class ProjectSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
       return Project.objects.filter(published=True)
 
    def lastmod(self, item): 
       return item.published_on

    def location(self, item):
        return reverse('portfolio:project_detail', args=[item.slug])

class PortfolioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['portfolio']

    def lastmod(self, item):
        try:
            return Project.objects.latest().date
        except:
            return None

    def location(self, item):
        return reverse('portfolio:project_list')
