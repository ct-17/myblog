from django.shortcuts import render
from django.views.generic import ListView
from blog.models import PostModel as Search_blog

class Search(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        if query is not None:
            return Search_blog.objects.search(query)  #and Search_internet.objects.search(query) and Search_mobile.objects.search(query)
        return False
        # return Search_blog.objects.featured()
