# Generated by Django 4.0.6 on 2024-05-04 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='ahortname',
            new_name='shortname',
        ),
    ]
