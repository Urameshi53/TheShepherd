# Generated by Django 5.0.2 on 2024-08-14 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0005_remove_discussion_course_student_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='topic',
            field=models.CharField(default='Programming', max_length=60),
        ),
    ]
