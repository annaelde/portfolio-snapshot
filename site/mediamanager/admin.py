from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Image

class MediaAdmin(GenericStackedInline):
    model = Image
    extra = 0
    exclude = ('extension','height','width',)