"""
Defines the list view and detail view for the blog.
"""
from django.http import Http404
from django.views.generic import DetailView, ListView

from mediamanager.helpers import create_thumbnail
from taggit.models import Tag

from .models import Post, TaggedPost


class PostListView(ListView):
    """
    Returns a list of all published posts sorted by date
    """
    model = Post
    template_name = 'blog/list.html'
    paginate_by = 4

    def get_queryset(self):
        """
        Return published posts
        """
        try:
            tag = self.request.GET.get('tag')
        except:
            tag = None
        
        # Check if user is authenticated
        if self.request.user.is_authenticated:
            post_list = Post.objects.all()
        else:
            post_list = Post.objects.filter(published=True)
        
        # Check if tag was selected
        if tag is not None:
            return post_list.filter(tags__slug=tag)
        else:
            return post_list.order_by('-published_on')
            
    def get_context_data(self, **kwargs):
        """
        Add tag information to requests for tag filtering.
        """
        context = super(PostListView, self).get_context_data(**kwargs)
        # Get tag info
        try:
            tag = self.request.GET.get('tag')
        except:
            tag = None
        if tag is not None:
            context['tag_slug'] = tag
            try: 
                context['tag_name'] = Tag.objects.get(slug=tag).name
            except:
                context['tag_name'] = None
        # Get the tag cloud
        context['tag_cloud'] = Post.tags.most_common()
        return context

class PostDetailView(DetailView):
    """
    Returns a single post.
    """
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        """
        Returns a blog post.
        """
        self.object = self.get_object()
        
        #Render blog post only if post is published, but render draft if user is logged in
        if not self.object.published and not request.user.is_authenticated:
            raise Http404()
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Add banner sourceset and related posts to context data.
        """
        context = super().get_context_data(**kwargs)

        # Add srcset for responsive banners
        if self.object.responsive_banners is True:
            context['banner_set'] = self.create_banner_set()

        #Get a max of three related posts
        related_posts = self.object.tags.similar_objects()
        for post in related_posts:
            if not post.published:
                related_posts.remove(post)
        if len(related_posts) >= 1:
            context['related_posts'] = related_posts[:3]
            for post in context['related_posts']:
                try:
                    post.default_banner.thumbnail
                except:
                    if post.default_banner:
                        create_thumbnail(post.default_banner, 150, 300)
        return context

    def create_banner_set(self):
        """
        Creates a responsive image srcset
        """
        obj = self.object
        banner_set = []
        if obj.large_banner:
            banner_set.append(' '.join([obj.large_banner.media_file.url, str(obj.large_banner.media_file.width)]) + 'w')
        if obj.medium_banner:
            banner_set.append(' '.join([obj.medium_banner.media_file.url, str(obj.medium_banner.media_file.width)]) + 'w')
        if obj.small_banner:
            banner_set.append(' '.join([obj.small_banner.media_file.url, str(obj.small_banner.media_file.width)]) + 'w')
        banner_set = banner_set = ', '.join(banner_set)
        return banner_set
