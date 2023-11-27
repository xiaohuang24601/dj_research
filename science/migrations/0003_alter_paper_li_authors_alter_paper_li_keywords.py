# Generated by Django 4.0.3 on 2023-04-26 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('science', '0002_delete_organization_paper_json_str_paper_li_authors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='li_authors',
            field=models.ManyToManyField(to='science.scholar', verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='li_keywords',
            field=models.ManyToManyField(to='science.keywords', verbose_name='关键词(领域)'),
        ),
    ]