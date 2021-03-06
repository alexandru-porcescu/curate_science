# Generated by Django 2.1.1 on 2018-10-26 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curate', '0017_auto_20181023_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='keyfigure',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='keyfigure',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='pdf_url',
            field=models.URLField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='article',
            name='html_url',
            field=models.URLField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='article',
            name='preprint_url',
            field=models.URLField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='study',
            name='replication_of',
            field=models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
        )
    ]
