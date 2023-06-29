# Generated by Django 4.1.5 on 2023-06-29 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_alter_user_department_alter_user_uni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='department', to='core.department'),
        ),
    ]