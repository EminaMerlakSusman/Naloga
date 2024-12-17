# Generated by Django 5.1.4 on 2024-12-16 22:37

from django.db import migrations

from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    Group.objects.get_or_create(name='admin_user')
    Group.objects.get_or_create(name='normal_user')


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_question_owner'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
