# Generated by Django 4.1.5 on 2023-04-27 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_alter_teammember_enrollmentno_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='fyp_panel',
        ),
    ]
