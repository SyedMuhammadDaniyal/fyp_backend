# Generated by Django 4.1.5 on 2023-01-16 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_project_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='faculty_no',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]
