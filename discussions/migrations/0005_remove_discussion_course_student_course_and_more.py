# Generated by Django 5.0.2 on 2024-08-14 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0004_remove_message_discussion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='course',
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.CharField(blank=True, default='Computer Science', max_length=60),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, default='0548932933', max_length=10),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.CharField(blank=True, default='KNUST', max_length=60),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='num_of_participants',
            field=models.IntegerField(blank=True, default=50),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='votes',
            field=models.IntegerField(blank=True, default=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='back_img',
            field=models.ImageField(blank=True, default='images/profiles/testimonial-1_wBDCxRj.jpg', upload_to='images/profiles'),
        ),
    ]
