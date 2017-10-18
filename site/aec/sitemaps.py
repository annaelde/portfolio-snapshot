"""
Imports app sitemaps and defines sitemap dictionary.
"""
from blog.sitemap import BlogSitemap, PostSitemap
from contact.sitemap import ContactSitemap
from home.sitemap import HomeSitemap
from portfolio.sitemap import PortfolioSitemap, ProjectSitemap

sitemaps = {
    'post': PostSitemap(),
    'blog': BlogSitemap(),
    'project': ProjectSitemap(),
    'portfolio': PortfolioSitemap(),
    'home' : HomeSitemap(),
    'contact' : ContactSitemap(),
}
