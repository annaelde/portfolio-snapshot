"""
Defines customized form for admin.
"""
from django.forms import ModelForm, RadioSelect, Textarea
from django.utils import six

from taggit.managers import TaggableManager
from taggit.utils import edit_string_for_tags

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


class ProjectAdminForm(ModelForm):
    """
    Customized admin form for Project admin.
    """
    def clean(self):
        cleaned_data = super().clean()
        external = cleaned_data.get('external_url')
        slug = cleaned_data.get('slug')

        if slug and external:
            msg = "You cannot use both an internal and external URL. Please remove one."
            self.add_error("slug", msg)
            self.add_error("external_url", '')
        elif not slug and not external:
            msg = "Either an internal or external URL is required to save this project."
            self.add_error("slug", msg)
            self.add_error("external_url", '')
        else:
            return cleaned_data

    class Meta:
        """
        Sets correct widgets, help text, and labels for fields.
        """
        model = Project
        fields = '__all__'

        widgets = {
            'published': RadioSelect,
            'description': Textarea(attrs={'rows': 2, 'cols': 85, 'maxlength': 160}),
            'snippet': Textarea(attrs={'rows': 3, 'cols': 90, 'maxlength': 1024}),
            'tags': TaggitAdminTextareaWidget(attrs={'rows': 1, 'cols': 90}),
        }

        help_texts = {
            'thumbnail': 'Recommended size: 400px by 200px.',
            'description': 'Maximum length is 160 characters.',
            'slug' : 'Should only include the slug.',
            'external_url': 'Should include the full URL.'
        }

        labels = {
            'published': 'Status',
            'external_url': 'External URL',
            'slug' : 'Internal URL'
        }
