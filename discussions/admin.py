from django.contrib import admin
from .models import Discussion, Comment, Student, Notification, Message
# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class DiscussionAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Student)
admin.site.register(Notification)
admin.site.register(Message)