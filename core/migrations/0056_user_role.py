# Generated by Django 4.1.5 on 2023-04-29 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_alter_user_phoneno'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('supervisor', 'supervisor'), ('student', 'student'), ('fyp_panel', 'fyp_panel')], max_length=20, null=True),
        ),
    ]
