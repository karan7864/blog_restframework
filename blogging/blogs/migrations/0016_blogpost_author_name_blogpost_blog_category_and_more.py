# Generated by Django 4.2.3 on 2023-08-07 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0015_newblog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='blog_category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='blogger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blogger', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='NewBlog',
        ),
    ]
