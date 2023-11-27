# Generated by Django 4.0.3 on 2023-05-04 08:48

from django.db import migrations, models
import science.models


class Migration(migrations.Migration):

    dependencies = [
        ('science', '0008_remove_scholar_id_from_site_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholar',
            name='h_index',
            field=models.FloatField(blank=True, default=science.models.gen_h_index, null=True, verbose_name='h指数'),
        ),
        migrations.AddField(
            model_name='scholar',
            name='referenced_count',
            field=models.IntegerField(blank=True, default=science.models.gen_referenced_count, null=True, verbose_name='被引用'),
        ),
    ]