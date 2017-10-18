"""
Describes the post model.
"""
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify

import markdown
from mediamanager.helpers import insert_images
from mediamanager.models import Image
from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import TaggedItemBase

PUBLISHED_CHOICES = (
    (False, 'Save as Draft'), 
    (True, 'Publish to Blog'),
)

BANNER_CHOICES = (
    (False, 'Use Default Banner'), 
    (True, 'Use Default and Responsive Banners'),
)

class PostTagManager(_TaggableManager):
    """
    TaggableManager with helper functions for posts.
    """
    def post_tags(self):
        """
        Returns a dictionary of tags and their slugs
        """
        return dict(zip(self.names(), self.slugs()))
    
class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey('Post')

class Post(models.Model):
    """
    A post in the blog.
    """
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    # Date-related
    published = models.BooleanField(default=False, choices=PUBLISHED_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    published_on = models.DateTimeField(blank=True, null=True)
    # Title-related
    title = models.CharField(max_length=64, default="")
    slug = models.SlugField(max_length=64, unique=True, db_index=True, default="")
    # Tags
    tags = TaggableManager(manager=PostTagManager, through=TaggedPost, blank=True)
    # Text content
    content = models.TextField(blank=True, default="")
    snippet = models.CharField(max_length=160, blank=True, default="")
    # Image related
    default_banner = models.ForeignKey(Image, blank=True, null=True, related_name='default_banner', on_delete=models.SET_NULL)
    images = GenericRelation(Image, related_query_name='post_images', content_type_field='content_type', object_id_field='object_id')
    # Responsive banners
    responsive_banners =  models.BooleanField(default=False, choices=BANNER_CHOICES)
    small_banner = models.ForeignKey(Image, blank=True, null=True, related_name='small_banner', on_delete=models.SET_NULL)
    medium_banner = models.ForeignKey(Image, blank=True, null=True, related_name='medium_banner', on_delete=models.SET_NULL)
    large_banner = models.ForeignKey(Image, blank=True, null=True, related_name='large_banner', on_delete=models.SET_NULL)

    class Meta:
        get_latest_by = 'published_on'

    def __str__(self):
        """
        Represent via title.
        """
        return self.title

    def get_author(self):
        """
        Returns author's full name
        """
        return self.author.first_name + ' ' + self.author.last_name

    def save(self, *args, **kwargs):
        """
        Make sure the slug is valid on saving.
        """
        if self.slug is None:
            self.slug = slugify(self.title)
        self.slug = slugify(self.slug)
        super(Post, self).save(*args, **kwargs)

    def markdown(self):
        """
        Process markdown and shortcodes into HTML.
        """
        processor = markdown.Markdown(extensions=['markdown.extensions.toc(title=Table of Contents, baselevel=2)',
                                                  'markdown.extensions.tables',
                                                  'markdown.extensions.fenced_code',
                                                  'markdown.extensions.codehilite'])
        content = insert_images(self, self.content)
        return processor.convert(content)