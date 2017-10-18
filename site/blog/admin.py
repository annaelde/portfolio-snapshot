"""
Admin panel for blog posts. Increases size of snippet widget
and makes the title prepopulate the slug.
"""
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from mediamanager.admin import MediaAdmin
from mediamanager.models import Image

from .forms import PostAdminForm
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MediaAdmin]
    list_display = ['title', 'author_name',
                    'created_on', 'published', 'published_on', ]
    fieldsets = (('Publishing Options',
                  {'fields': ('title', 'author', 'slug', 'published', 'published_on', 'tags',)}),
                 ('Content Options',
                  {'fields': ('content', 'snippet')}),
                 ('Image Options',
                  {'fields': ('default_banner', 'responsive_banners', 'small_banner', 'medium_banner', 'large_banner')}),
                 )

    def author_name(self, obj):
        """
        Displays author's full name in list view
        """
        return obj.get_author()

    author_name.short_description = 'Author'

    def get_form(self, request, obj=None, **kwargs):
        """
        Returns a customized post admin form.
        """
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)

        # Disable image fields when appropriate
        if obj is None:
            for banner in ('default_banner', 'small_banner', 'medium_banner', 'large_banner',):
                form.base_fields[banner].widget.attrs['disabled'] = True
        elif obj.responsive_banners is False:
            content = ContentType.objects.get_for_model(Post)
            form.base_fields['default_banner'].queryset = Image.objects.filter(
                object_id=obj.id, content_type=content.id)
            for banner in ('small_banner', 'medium_banner', 'large_banner',):
                form.base_fields[banner].widget.attrs['disabled'] = True
        else:
            content = ContentType.objects.get_for_model(Post)
            image_set = Image.objects.filter(
                object_id=obj.id, content_type=content.id)
            for banner in ('default_banner', 'small_banner', 'medium_banner', 'large_banner',):
                form.base_fields[banner].queryset = image_set

        return form
