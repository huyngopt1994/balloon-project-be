# Generated by Django 2.2.1 on 2019-05-19 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_source', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='price',
        ),
        migrations.AddField(
            model_name='transactions',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
