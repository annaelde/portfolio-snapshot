"""
Helper functions for use with models that integrate the media manager.
"""
from io import BytesIO
from os import path

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import slugify

from PIL import Image


def get_directory(instance: object) -> str:
    """
    Returns the directory used to store media files for this type of object.
    """
    app_dir = slugify(instance.content_object.__module__.split('.')[0])
    object_dir = slugify(instance.content_object.__str__().lower())
    return path.join('images', app_dir, object_dir)

def insert_images(instance: object, text: str) -> str:
    """
    Takes text input from an instance using the media manager
    and replaces all references to [slug] with a link.
    """
    from .models import Image

    content = ContentType.objects.get_for_model(instance)
    media = Image.objects.filter(object_id=instance.id, content_type=content.id)

    for media_file in media:
        token = ''.join(['[', media_file.slug, ']'])
        image = '"'.join(['<img src=', '/'.join([settings.MEDIA_URL, get_directory(media_file), (media_file.slug + media_file.extension)]),
                          ' alt=', media_file.alt_text, ' title=', media_file.title, '/>\n'])

        if media_file.caption != '':
            caption = ''.join(['<div class="media__caption">', media_file.caption, '</div>'])
            image = image + caption

        text = text.replace(token, image)

    return text

def roundTuple(*args: float) -> tuple:
    """
    Takes a tuple, rounds each float and casts to integer,
    returns a tuple.
    """
    rounded = list()
    for number in args: 
        rounded.append(int(round(number)))
    return tuple(rounded)

def crop_thumbnail(original: Image, target_width: float, target_height: float) -> Image:
    """
    Resizes and crops a thumbnail to the desired measurements
    """
    target_ratio = target_width / target_height
    original_ratio = original.width / original.height

    if target_ratio > original_ratio:
        scale = target_width / original.width
        crop_height = target_height / scale
        crop_width = original.width
        margin = (original.height - crop_height) / 2
        original = original.crop(roundTuple(0, margin, crop_width, margin + crop_height,))
    elif target_ratio < original_ratio:
        scale = target_height / original.height
        crop_height = original.height
        crop_width = target_width / scale
        margin = (original.width - crop_width) / 2
        original = original.crop(roundTuple(margin, 0, margin + crop_width, crop_height,))
        
    return original.resize((target_width, target_height,), Image.ANTIALIAS)

def create_thumbnail(instance: object, height: float, width: float):
    """
    Creates a thumbnail based on the height and width.
    """
    from .models import Thumbnail
    
    # Read original file into memory
    original_file = BytesIO(instance.media_file.file.read())
    # Open file as image
    image = Image.open(original_file)
    # Crop the image
    image_format = image.format
    image = crop_thumbnail(image, width, height)

    # Create a new file stream for the new file
    new_file = BytesIO()
    # Save the cropped file to the new stream
    image.save(new_file, image_format, quality=100)
    # Seek to beginning of the stream
    new_file.seek(0)

    # Create a file upload object to give to the media_file field and read the new_file stream into it
    file_upload = SimpleUploadedFile(''.join([instance.slug, '-tb', instance.extension]), new_file.read(), content_type=('image/' + instance.extension.replace('.','')))

    # Create the Thumbnail model instance
    tb = Thumbnail.objects.create(content_type=instance.content_type,
                                  object_id = instance.object_id,
                                  content_object = instance.content_object,
                                  title = instance.title,
                                  caption = instance.caption,
                                  alt_text = instance.alt_text,
                                  slug = '-'.join([instance.slug, 'tb']),
                                  extension = instance.extension,
                                  height = height,
                                  width = width,
                                  original = instance,
                                  media_file = file_upload)

    # Close the buffers
    original_file.close()
    new_file.close()
    image.close()
