from django.views.generic.base import TemplateView
from blog.views import PostListView
from home.models import SkillSet

class HomeView(TemplateView):
    """
    Defines the context for the homepage.
    """
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        """
        Adds skill sets and most recent post list to
        the context of the home view
        """
        context = super().get_context_data(**kwargs)
        context['post_list'] = PostListView(request=self.request).get_queryset()[:2]
        context['skill_sets'] = SkillSet.objects.all()
        return context