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

from .models import Request, Contribution


class IndexView(generic.ListView):
    template_name = "sliders/index.html"
    context_object_name = "sliders"
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
        context['requests'] = Request.objects.all()
        context['contributions'] = Contribution.objects.all()
        

        return context

class DetailView(generic.DetailView):
    model = Request
    template_name = "sliders/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['student'] = Student.objects.filter(user=self.request.user)[0]
        context['requests'] = Request.objects.filter(requester_id=self.kwargs['pk'])
        context['contributions'] = Contribution.objects.filter(request_id=self.kwargs['pk'])
        context['all_requests'] = Request.objects.all()
        
        return context