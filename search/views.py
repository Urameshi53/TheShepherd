from typing import Any, Dict
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core.paginator import Paginator


from repository.models import File
from discussions.models import Discussion, Student
#from .mega import Search
from .finder import Search
from .forms import SearchForm



class IndexView(generic.ListView):
    template_name = "search/index.html"
    context_object_name = "search"
    #paginate_by = 3
    model = File
    #form = SearchForm()

    def get_queryset(self):
        return File.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        #context['discussions'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        #context['discussions'] = Search.get_result()        
        context['files'] = File.objects.all()
        context['student'] = Student.objects.filter(user=self.request.user)[0]
        context['form'] = SearchForm(self.request.GET)

        #print(context['form'].is_valid())
        if context['form'].is_valid():
            s = Search()
            query = context['form'].cleaned_data['query']
            context['results'] = s.find(query)
            #print(context['results'])

        return context

'''
class DetailView(generic.DetailView):
    model = File
    template_name = "repository/details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['repository'] = File.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['comments'] = Comment.objects.filter(File_id=self.kwargs['pk'])#blog__pk=9)#context['blogs'].values('id'))

        return context
    

def post(request, discussion_id):
    discussion = get_object_or_404(discussion, pk=discussion_id)
    new_comment = Comment()
    new_comment.comment_text = request.POST['comment_text']
    new_comment.pub_date = datetime.datetime.now()
    new_comment.author = request.user
    new_comment.discussion_id = discussion_id
    new_comment.save()
    discussion.comment_set.add(new_comment)
    return HttpResponseRedirect(f"/repository/{discussion_id}/")
'''
    
def search(request):
    form = ''#SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Discussion.objects.filter(title__contains=query)
    
    return render(request, 'search/search.html', {'form':form, 'results': results})


