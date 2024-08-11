from django.db import models
from discussions.models import Student
from django.utils.timezone import now

# Create your models here.

class File(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField()
    pub_date = models.DateTimeField(blank=False, default=now)
    file_name = models.CharField(max_length=60, blank=True, default='Book')
    back_img = models.ImageField(blank=True, upload_to="images/books", default='images/597_1.jpg')

    def __str__(self):
        return self.file_name

