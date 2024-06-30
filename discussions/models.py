from django.db import models
from django.contrib.auth.models import User
from django.forms import DateInput, ModelForm
from django.utils.timezone import now


class Student(models.Model):
    friend = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    back_img = models.ImageField(blank=True, upload_to="images/profiles", default='images/597_1.jpg')

    def __str__(self) -> str:
        return self.user.username
    
class Discussion(models.Model):
    creator = models.ForeignKey(Student, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(blank=False, default=now)
    content = models.CharField(max_length=200)
    votes = models.IntegerField()
    course = models.CharField(max_length=60)
    num_of_participants = models.IntegerField()

    def __str__(self) -> str:
        return self.content
    
class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    comment_text = models.TextField()

    def __str__(self) -> str:
        return self.comment_text

class CommentForm(ModelForm):
    class Meta:
        model = Comment 
        fields = ["comment_text"]



