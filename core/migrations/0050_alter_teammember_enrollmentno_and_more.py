# Generated by Django 4.1.5 on 2023-04-26 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_alter_user_phoneno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='enrollmentno',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='rollno',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='seatno',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
