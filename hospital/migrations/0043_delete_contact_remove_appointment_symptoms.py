# Generated by Django 4.1.1 on 2022-10-01 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0042_contact'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='symptoms',
        ),
    ]
