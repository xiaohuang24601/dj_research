# Generated by Django 4.0.3 on 2023-05-04 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('science', '0007_alter_keywords_created_at_alter_scholar_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholar',
            name='id_from_site',
        ),
        migrations.RemoveField(
            model_name='scholar',
            name='organization_02',
        ),
        migrations.RemoveField(
            model_name='scholar',
            name='organization_03',
        ),
        migrations.RemoveField(
            model_name='scholar',
            name='year',
        ),
    ]
