from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateInput, ModelForm
from django.utils.timezone import now


class Student(models.Model):
    friend = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, default='0548932933', blank=True)
    school = models.CharField(max_length=60, default='KNUST', blank=True)
    course = models.CharField(max_length=60, default='Computer Science', blank=True)
    back_img = models.ImageField(blank=True, upload_to="images/profiles", default='images/profiles/testimonial-1_wBDCxRj.jpg')

    def __str__(self) -> str:
        return self.user.username
    
    
class Discussion(models.Model):
    creator = models.ForeignKey(Student, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(blank=False, default=now)
    content = models.CharField(max_length=200)
    description = models.CharField(max_length=1024, blank=True, default='This is just a sample')
    topic = models.CharField(max_length=60,blank=False, default='Programming')
    img = models.ImageField(blank=True, upload_to="images", null=True)
    likes = models.IntegerField(blank=True, default=100)
    dislikes = models.IntegerField(blank=True, default=100)
    num_of_participants = models.IntegerField(blank=True, default=50)

    def was_published_recently(self):
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

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


class Message(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    message_text = models.TextField()

    def __str__(self) -> str:
        return self.message_text


class Notification(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    content = models.TextField()

    def __str__(self) -> str:
        return self.content