# Generated by Django 4.1.5 on 2023-04-26 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_user_phoneno'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email', 'deleted_at')},
        ),
    ]
