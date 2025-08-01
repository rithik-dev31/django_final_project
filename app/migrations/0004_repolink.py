# Generated by Django 5.2.4 on 2025-07-30 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_jobopenings_jobopening'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repolink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('repo_url', models.URLField(max_length=500)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.section')),
            ],
        ),
    ]
