from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6

    def items(self):
       return Post.objects.filter(published=True)
 
    def lastmod(self, item): 
       return item.published_on

    def location(self, item):
        return reverse('blog:post_detail', args=[item.slug])

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ['blog']

    def lastmod(self, item):
        try:
            return Post.objects.latest().published_on
        except:
            return None
    
    def location(self, item):
        return reverse('blog:post_list')
