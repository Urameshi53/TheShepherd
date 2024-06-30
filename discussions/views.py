from typing import Any, Dict
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core.paginator import Paginator

from sliders.models import Request, Contribution
from .models import Student, Discussion, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = "discussions/index.html"
    context_object_name = "discussions"
    paginate_by = 5
    model = Discussion

    def get_queryset(self):
        return Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['latest'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['students'] = Student.objects.all()
        context['requests'] = Request.objects.all()

        if self.request.user.is_authenticated:
            context['student'] = Student.objects.filter(user=self.request.user)[0]

        return context

class DetailView(generic.DetailView):
    model = Discussion
    template_name = "discussions/details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['discussions'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['latest'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['comments'] = Comment.objects.filter(discussion_id=self.kwargs['pk'])#blog__pk=9)#context['blogs'].values('id'))
        context['form'] = CommentForm()

        if self.request.user.is_authenticated:
            context['student'] = Student.objects.filter(user=self.request.user)[0]

        return context
    

def like(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion.likes += 1


def post_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    new_comment = Comment()
    new_comment.comment_text = request.POST['comment_text']
    new_comment.pub_date = datetime.datetime.now()
    new_comment.author = Student.objects.filter(user_id=request.user.id)[0]
    new_comment.discussion_id = discussion_id
    new_comment.save()
    discussion.comment_set.add(new_comment)
    return HttpResponseRedirect(f"/discussions/{discussion_id}/")

    
def search(request):
    form = ''#SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Discussion.objects.filter(title__contains=query)
    
    return render(request, 'search/search.html', {'form':form, 'results': results})


