from typing import Any, Dict
from django.db import models
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from .models import Project, Supervisor, ProjectFile
from sliders.models import Request
from discussions.models import Student, Discussion, Comment
from .forms import UploadFileForm
from repository.models import File

from .forms import ProjectForm

class IndexView(generic.ListView):
    template_name = "home/index.html"
    context_object_name = "projects"
    #paginate_by = 3
    model = Project

    def get_queryset(self):
        return Project.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['files'] = File.objects.filter(owner_id=self.request.user.id)
        context['student'] = Student.objects.filter(user=self.request.user)[0]
        context['latest'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['requests'] = Request.objects.all()[:5]
        #context['project_files'] = ProjectFile.objects.filter(project_id=self.kwargs['pk'])
        # context['form'] = UploadFileForm

        return context



class DetailView(generic.DetailView):
    model = Project
    template_name = "home/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['discussions'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['comments'] = Comment.objects.filter(discussion_id=self.kwargs['pk'])#blog__pk=9)#context['blogs'].values('id'))
        context['form'] = UploadFileForm()
        context['files'] = File.objects.all()[:5]
        context['requests'] = Request.objects.all()
        context['latest'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['trending'] = File.objects.all()[:5]
        context['projects'] = Project.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

        if self.request.user.is_authenticated:
            context['student'] = Student.objects.filter(user=self.request.user)[0]

        return context
    
def create(request):
    form = ProjectForm()
    if request.method == 'POST':
        topic = request.POST.get('topic')
        description = request.POST.get('description')
        research = request.POST.get('research')
        
        new_project = Project()
        new_project.topic = topic
        new_project.description = description
        new_project.research_area = research
        new_project.pub_date = timezone.now()
        new_project.save()
        return redirect('home')
    return render(request, 'accounts/login.html', {'form':form})#, RequestContext(request))


def contribute(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    new_file = ProjectFile()
    new_file.file = request.POST['file']
    new_file.pub_date = timezone.now()
    new_file.save()
    project.projectfile_set.add(new_file)
    return HttpResponseRedirect(f"/projects/{project_id}/")