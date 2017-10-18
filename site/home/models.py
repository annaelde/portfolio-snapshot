import markdown
from django.db import models
from django.contrib.postgres.fields import ArrayField
from solo.models import SingletonModel


class Introduction(SingletonModel):
    """
    Defines introduction on homepage using singleton model.
    """
    biography = models.TextField()
    post_script = models.TextField()

    def __unicode__(self):
        return u"Introduction"

    def bio_markdown(self):
        processor = markdown.Markdown(extensions=['markdown.extensions.fenced_code', 
                                                  'markdown.extensions.codehilite'])
        return processor.convert(self.biography)

    def ps_markdown(self):
        processor = markdown.Markdown()
        return processor.convert(self.post_script)

    class Meta:
        verbose_name = "Introduction"


class SkillSet(models.Model):
    """
    Defines a skillset.
    """
    title = models.CharField(max_length=64, default="")
    skills = ArrayField(models.CharField(max_length=64, blank=True), size=12,)

    def __str__(self):
        return self.title
