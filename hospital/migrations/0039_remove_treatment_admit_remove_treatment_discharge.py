# Generated by Django 4.1.1 on 2022-09-30 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0038_patient_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatment',
            name='admit',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='discharge',
        ),
    ]
