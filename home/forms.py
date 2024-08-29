from discussions.models import Discussion
from django import forms 
from .models import Project, Supervisor

class ProjectForm(forms.Form):
    topic = forms.CharField(label='Project Topic', widget=forms.TextInput
                    (attrs={'class':'form-control', 'name':'topic', 'placeholder':'Project Topic'}))
    description = forms.CharField(label='Project Topic', widget=forms.Textarea
                    (attrs={'class':'form-control', 'name':'description', 'placeholder':'Description'}))
    research_area = forms.CharField(label='Research Area', widget=forms.TextInput
                    (attrs={'class':'form-control', 'name':'research', 'placeholder':'Research Area'}))


class UploadFileForm(forms.Form):
    file = forms.FileField()