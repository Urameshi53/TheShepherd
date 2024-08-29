from django.db import models
from discussions.models import Student
from django.utils import timezone


s = Student.objects.filter(pk=1)

class Supervisor(models.Model):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=60)
    email = models.EmailField()
    department = models.CharField(max_length=60)
    degree = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    topic = models.CharField(max_length=120)
    description = models.CharField(max_length=2048, default='Description')
    research_area = models.CharField(max_length=60)
    pub_date = models.DateTimeField(blank=True, null=True, default=timezone.now())
    rating = models.FloatField(blank=True, null=True, default=4.3)
    back_img = models.ImageField(blank=True, upload_to="images/backs", null=True, default='assets/img/user.png')

    def __str__(self) -> str:
        return self.topic


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self) -> str:
        return self.file.name


