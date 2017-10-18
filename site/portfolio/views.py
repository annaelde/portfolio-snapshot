"""
Defines views for portfolio.
"""
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import DetailView, ListView
from django.forms.models import model_to_dict
from taggit.models import Tag

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/list.html'

    def get(self, request, *args, **kwargs):
        """
        Overrides to include logic for AJAX requests.
        """
        if request.is_ajax():
            self.template_name = 'portfolio/inner_list.html'
            self.object_list = self.get_queryset()
            allow_empty = True
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            return super(ProjectListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return published projects ordered by date and category
        """
        try:
            tags = self.request.GET.getlist('tag')
        except:
            tags = None

        if tags:
            tags = list(set(tags))
            project_query = Project.objects.all()
            for tag in tags:
                project_query = project_query.filter(tags__slug=tag)
            return project_query
        else:
            return Project.objects.filter(published=True).order_by('category', '-date')

    def get_context_data(self, **kwargs):
        """
        Add tags to context.
        """
        context = super(ProjectListView, self).get_context_data(**kwargs)
        # Add tags for filtering
        context['project_tags'] = Project.tags.most_common()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/detail.html'

    def get(self, request, *args, **kwargs):
        """
        Render project only if project is published,
        but render draft if user is logged in
        """
        self.object = self.get_object()
        if not self.object.published and not request.user.is_authenticated:
            raise Http404()
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
