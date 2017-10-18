"""
A generic media model for organizing file uploads and
managing overwriting and deletion of files.
"""
from enum import Enum
from os import path, remove, rename

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .helpers import get_directory


class UPLOAD(Enum):
    """
    Enumeration for state of a media upload.
    """
    UNKNOWN = 0
    NEW = 1
    OVERWRITE = 2
    SAME = 3

class SLUG(Enum):
    """
    Enumeration for state of a media slug.
    """
    UNKNOWN = 0
    EMPTY = 1
    UNIQUE = 2
    DUPLICATE = 3
    SAME = 4

class FILE(Enum):
    """
    Enumeration for state of a media file.
    """
    UNKNOWN = 0
    UNIQUE = 1
    DUPLICATE = 2
    SAME = 3

class Media(models.Model):
    # Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # Meta Data
    title = models.CharField(max_length=128, default='', blank=True)
    caption = models.CharField(max_length=128, default='', blank=True)
    alt_text = models.CharField(max_length=128, default='', blank=True)
    # File Fields
    slug = models.SlugField(max_length=64, db_index=True, default='', blank=True)
    extension = models.CharField(max_length=16, default='', blank=True)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    media_file = models.ImageField(height_field='height', width_field='width')

    class Meta:
        abstract = True


class Image(Media):
    """
    An image file
    """
    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """
        Saves the model with a unique file name in the appropriate directory,
        renaming the model with the chosen slug when possible.
        """
        # Initialize media file states
        upload_state = UPLOAD.UNKNOWN
        slug_state = SLUG.UNKNOWN
        file_state = FILE.UNKNOWN

        # Name the media file
        current = self.media_file

        # Get file directory
        directory = get_directory(self)

        # Get a copy of the model from the database
        try:
            original = Image.objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            original = None

        # Get name of uploaded file -- {slug}.{extension}
        file_name = path.basename(current.name)

        # Get the slug, extension and file path from uploaded file
        file_slug, self.extension = path.splitext(file_name)
        file_path = path.join(directory, (file_slug + self.extension))

        # Determine the upload state
        if original is None:
            upload_state = UPLOAD.NEW
        elif original.media_file != current:
            upload_state = UPLOAD.OVERWRITE
        else:
            upload_state = UPLOAD.SAME

        # Determine the slug state
        if self.slug == '':
            slug_state = SLUG.EMPTY
        elif upload_state != UPLOAD.NEW and self.slug == original.slug and self.extension == original.extension:
            slug_state = SLUG.SAME
        else:
            try:
                media = Image.objects.get(slug=self.slug, extension=self.extension)
            except ObjectDoesNotExist:
                media = None
            if media is None:
                slug_state = SLUG.UNIQUE
            else:
                slug_state = SLUG.DUPLICATE

        # Determine the file state
        if upload_state == UPLOAD.SAME:
            file_state = FILE.SAME
        else:
            try:
                media = Image.objects.get(media_file=file_path)
            except ObjectDoesNotExist:
                media = None
            if media is None:
                file_state = FILE.UNIQUE
            else:
                file_state = FILE.DUPLICATE

        # Raise an error if something is still unknown for some reason
        if slug_state == SLUG.UNKNOWN or file_state == FILE.UNKNOWN or upload_state == UPLOAD.UNKNOWN:
            raise models.FieldError('The file could not be uploaded.')

        # Name the file according to the slug state and file state
        if slug_state == SLUG.UNIQUE:
            current.name = path.join(directory, (self.slug + self.extension))
        elif slug_state == SLUG.EMPTY and file_state != FILE.DUPLICATE:
            self.slug = file_slug
            current.name = file_path
        elif slug_state == SLUG.EMPTY:
            current.name = current.storage.get_available_name(file_path)
            self.slug, self.extension = path.splitext(path.basename(current.name))
        elif slug_state == SLUG.DUPLICATE:
            current.name = current.storage.get_available_name(path.join(directory, (self.slug + self.extension)))
            self.slug, self.extension = path.splitext(path.basename(current.name))
        elif slug_state == SLUG.SAME:
            current.name = path.join(directory, (self.slug + self.extension))

        # Determine which files to rename/delete manually
        if upload_state == UPLOAD.SAME:
            rename(path.join(settings.MEDIA_ROOT, original.media_file.name), path.join(settings.MEDIA_ROOT, current.name))
        elif upload_state == UPLOAD.OVERWRITE:
            remove(path.join(settings.MEDIA_ROOT, original.media_file.name))

        # Delete thumbnails if the file has been changed in any way
        if hasattr(self, 'thumbnail') and (upload_state != UPLOAD.NEW or slug_state != SLUG.SAME):
            self.thumbnail.delete()

        # Close the original file if open
        if original is not None:
            original.media_file.close()

        super(Image, self).save(*args, **kwargs)

    class Meta:
        """
        Meta information for the Image class.
        """
        verbose_name = 'image'
        verbose_name_plural = 'images'

class Thumbnail(Media):
    original = models.OneToOneField(Image, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Saves the model in the correct directory (/tb/)
        """
        directory = path.join(get_directory(self), 'tb')
        self.media_file.name = path.join(directory, self.media_file.name)
        super(Thumbnail, self).save(*args, **kwargs)

    class Meta:
        """
        Meta information for the Thumbnail class.
        """
        verbose_name = 'thumbnail'
        verbose_name_plural = 'thumbnails'

@receiver(post_delete, sender=Image)
@receiver(post_delete, sender=Thumbnail)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Media` object is deleted.
    """
    if instance.media_file:
        if path.isfile(instance.media_file.path):
            remove(instance.media_file.path)
