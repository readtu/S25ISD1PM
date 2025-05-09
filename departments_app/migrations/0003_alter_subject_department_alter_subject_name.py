# Generated by Django 5.1.4 on 2025-04-30 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments_app', '0002_alter_subject_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='departments_app.department'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
