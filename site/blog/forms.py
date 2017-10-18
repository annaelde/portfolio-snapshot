"""
Defines customized form for admin.
"""
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, ModelForm, RadioSelect, Textarea
from django.utils import six

from taggit.managers import TaggableManager
from taggit.utils import edit_string_for_tags

from .models import Post


class AuthorModelChoiceField(ModelChoiceField):
    """
    Field that displays username as full name.
    """
    def label_from_instance(self, obj):
        return obj.get_full_name()

class TaggitAdminTextareaWidget(Textarea):
    """
    Redefines Taggit widget to use Textarea.
    """
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
        return super(TaggitAdminTextareaWidget, self).render(name, value, attrs)

class PostAdminForm(ModelForm):
    """
    Customized admin form for Post admin.
    """
    author = AuthorModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        """
        Sets correct widgets, help text, and labels for fields.
        """
        model = Post
        fields = '__all__'

        widgets = {
            'published': RadioSelect,
            'responsive_banners': RadioSelect,
            'content' : Textarea(attrs={'rows':30, 'cols':90}),
            'snippet' : Textarea(attrs={'rows':3, 'cols':90, 'maxlength': 160}),
            'tags' : TaggitAdminTextareaWidget(attrs={'rows': 1, 'cols': 90}),
        }

        help_texts = {
            'thumbnail' : 'Recommended size: 300px by 100px.',
            'responsive_banners' : 'Save for changes to take effect.',
            'default_banner' : 'The default banner\'s meta-data, such as alt-text, is used for all banner images.',
            'small_banner' : 'Recommended width: 600px or smaller.',
            'medium_banner' : 'Recommended width: about 1200px.',
            'large_banner' : 'Recommended width: 1600px or larger.',
            'snippet' : 'Maximum length is 160 characters.',
        }

        labels = {
            'responsive_banners' : 'Use responsive banners?',
            'published' : 'Status',
        }
