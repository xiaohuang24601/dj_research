# Generated by Django 4.0.3 on 2023-04-26 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('science', '0006_alter_paper_json_str_alter_scholar_json_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywords',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='scholar',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
    ]
