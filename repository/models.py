from django.db import models
from discussions.models import Student
from django.utils.timezone import now

# Create your models here.

class File(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField()
    pub_date = models.DateTimeField(blank=False, default=now)

    def __str__(self):
        return self.file.name

