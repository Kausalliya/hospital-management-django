# Generated by Django 2.2.6 on 2022-10-05 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0043_delete_contact_remove_appointment_symptoms'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='absent',
            field=models.BooleanField(default=False),
        ),
    ]
