# Generated by Django 4.1.5 on 2023-05-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_merge_20230429_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='marks',
            field=models.FloatField(blank=True, null=True),
        ),
    ]