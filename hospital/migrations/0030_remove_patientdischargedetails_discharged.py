# Generated by Django 4.1.1 on 2022-09-29 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0029_patient_discharged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdischargedetails',
            name='discharged',
        ),
    ]
