# Generated by Django 5.0.2 on 2024-08-04 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_file_owner_file_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='back_img',
            field=models.ImageField(blank=True, default='images/597_1.jpg', upload_to='images/books'),
        ),
    ]