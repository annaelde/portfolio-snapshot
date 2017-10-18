import markdown
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import TaggedItemBase
from mediamanager.models import Image
from mediamanager.helpers import insert_images

class ProjectTagManager(_TaggableManager):
    """
    TaggableManager with helper functions for projects.
    """
    def post_tags(self):
        """
        Returns a dictionary of tags and their slugs
        """
        return dict(zip(self.names(), self.slugs()))
    
class TaggedProject(TaggedItemBase):
    content_object = models.ForeignKey('Project', on_delete=models.CASCADE)

class Project(models.Model):
    """
    A project in the portfolio
    """
    # Constants
    WEB_CATEGORY = 1
    PROGRAMMING_CATEGORY = 2
    GAME_CATEGORY = 3
    CATEGORY_CHOICES = ((WEB_CATEGORY, 'Web Development'),
                        (PROGRAMMING_CATEGORY, 'Programming'),
                        (GAME_CATEGORY, 'Game Development'),)

    PUBLISHED_CHOICES = (
        (False, 'Save as Draft'), 
        (True, 'Publish to Portfolio'),
    )
    # Basic Info
    title = models.CharField(max_length=64, default="")
    subtitle = models.CharField(max_length=64, blank=True, default="")
    date = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False, choices=PUBLISHED_CHOICES)
    slug = models.SlugField(max_length=64, unique=True, db_index=True, blank=True, default="")
    external_url = models.URLField(blank=True, default="")
    repository = models.URLField(blank=True, default="")

    # Categorization
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=WEB_CATEGORY)
    tags = TaggableManager(manager=ProjectTagManager, through=TaggedProject, blank=True)

    # Portfolio Description (Markdown Supported)
    snippet = models.CharField(max_length=1024, blank=True, default="")

    # Meta Description
    description = models.CharField(max_length=160, blank=True, default="")

    # Content (Markdown Supported)
    content = models.TextField(blank=True, default="")

    # Images
    thumbnail = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)
    images = GenericRelation(Image, related_query_name='project_images', content_type_field='content_type', object_id_field='object_id')

    class Meta:
        get_latest_by = 'date'

    # Methods
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        self.slug = slugify(self.slug)
        super(Project, self).save(*args, **kwargs)

    def content_formatted(self):
        md = markdown.Markdown(extensions=['markdown.extensions.tables',
                                           'markdown.extensions.fenced_code',
                                           'markdown.extensions.codehilite'])
        content = insert_images(self, self.content)
        return md.convert(self.content)

    def snippet_formatted(self):
        md = markdown.Markdown(extensions=['markdown.extensions.fenced_code',
                                           'markdown.extensions.codehilite'])
        return md.convert(self.snippet)

    # Meta
    def __str__(self):
        return self.title
