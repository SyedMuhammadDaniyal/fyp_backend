# Generated by Django 4.1.5 on 2023-01-16 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_supervisor_faculty_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('milestone_name', models.CharField(max_length=75)),
                ('document_submissin_date', models.DateField()),
                ('milestone_defending_date', models.DateField()),
                ('milestone_details', models.CharField(max_length=500)),
                ('fyp_panel', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.fyppanel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
