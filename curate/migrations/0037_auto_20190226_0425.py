# Generated by Django 2.1.7 on 2019-02-26 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curate', '0036_author_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='author',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='author',
            name='middle_name',
        ),
    ]
