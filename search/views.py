from django.shortcuts import render
from django.views.generic import ListView
from blog.models import PostModel as Search_blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models import Q

class Search(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(*args, **kwargs)
        top_list = Search_blog.objects.all().annotate(total_like = Count('like')).order_by('-total_like')[:3]
        query = self.request.GET.get('q')
        context['query'] = query
        context.update({
            'top_list': top_list
        })
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Search_blog.objects.search(query)
        return False

        
