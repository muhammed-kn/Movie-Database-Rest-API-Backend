# Generated by Django 3.2.9 on 2021-11-06 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20211107_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='downvote',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='upvote',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
