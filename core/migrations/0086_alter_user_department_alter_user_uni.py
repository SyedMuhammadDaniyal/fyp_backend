# Generated by Django 4.1.5 on 2023-06-17 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0085_user_uni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='department', to='core.department'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uni',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.university'),
        ),
    ]
