# Generated by Django 3.2.3 on 2021-05-24 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='movie',
        ),
    ]
