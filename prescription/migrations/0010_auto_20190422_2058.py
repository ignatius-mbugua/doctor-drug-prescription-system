# Generated by Django 2.1.7 on 2019-04-22 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0009_patientdetail_medicine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetail',
            name='medicine',
            field=models.CharField(blank=True, choices=[('Medicine 1', 'medicine 1'), ('Medicine 2', 'medicine 2'), ('Medicine 3', 'medicine 3')], max_length=20),
        ),
    ]
