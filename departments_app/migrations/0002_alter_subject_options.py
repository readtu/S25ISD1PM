# Generated by Django 5.1.4 on 2025-04-28 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departments_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['code']},
        ),
    ]
