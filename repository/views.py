from typing import Any, Dict
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core.paginator import Paginator
from django.utils import timezone

from .forms import UploadFileForm
from .models import File
from sliders.models import Request
from discussions.models import Student, Discussion

class IndexView(generic.ListView):
    template_name = "repository/index.html"
    context_object_name = "repository"
    #paginate_by = 3
    model = File

    def get_queryset(self):
        return File.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['files'] = File.objects.filter(owner_id=self.request.user.id)
        context['student'] = Student.objects.filter(user=self.request.user)[0]
        context['latest'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['requests'] = Request.objects.all()[:5]
        context['trending'] = File.objects.all()[:5]
        context['form'] = UploadFileForm

        return context



def upload_file(request, owner_id):
    owner_ = get_object_or_404(Student, pk=owner_id)
    new_file = File()
    new_file.file = request.POST['file']
    new_file.pub_date = timezone.now()
    new_file.save()
    owner_.file_set.add(new_file)
    return HttpResponseRedirect(f"/repository/")
