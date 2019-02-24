# Generated by Django 2.1.7 on 2019-02-20 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curate', '0024_auto_20190219_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='platform_invites',
        ),
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(choices=[('ORIGINAL', 'original'), ('CONCEPTUAL', 'conceptual'), ('REPLICATION', 'replication'), ('REPRODUCIBILITY', 'reanalysis - reproducibility'), ('META_ANALYSIS', 'reanalysis - meta-analysis'), ('META_RESEARCH', 'reanalysis - meta-research'), ('COMMENTARY', 'commentary')], max_length=255),
        ),
    ]
