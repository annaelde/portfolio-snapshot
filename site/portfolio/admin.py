"""
Defines admin panel for portfolio projects.
"""
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms import RadioSelect, Textarea
from django.utils import six

from mediamanager.admin import MediaAdmin
from mediamanager.models import Image
from taggit.managers import TaggableManager
from taggit.utils import edit_string_for_tags

from .forms import ProjectAdminForm
from .models import Project


class TaggitAdminTextareaWidget(Textarea):
    """
    Redefines Taggit widget to use Textarea.
    """

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags(
                [o.tag for o in value.select_related("tag")])
        return super(TaggitAdminTextareaWidget, self).render(name, value, attrs)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MediaAdmin]
    list_display = ['title', 'category', 'date', 'published', ]
    fieldsets = (('Publishing Options',
                  {'fields': ('title', 'subtitle', 'category', 'tags', 'date', 'published', 'description')}),
                 ('Location Options',
                  {'fields': ('slug', 'external_url', 'repository')}),
                 ('Content Options',
                  {'fields': ('content', 'snippet')}),
                 ('Image Options',
                  {'fields': ('thumbnail',)}),
                 )

    def get_form(self, request, obj=None, **kwargs):
        """
        Returns customized project admin form.
        """
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)

        # Disable image fields on new model
        if obj is None:
            form.base_fields['thumbnail'].widget.attrs['disabled'] = True
        else:
            content = ContentType.objects.get_for_model(Project)
            form.base_fields['thumbnail'].queryset = Image.objects.filter(
                object_id=obj.id, content_type=content.id)
        return form
