# Generated by Django 5.1.4 on 2025-04-29 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('semesters_app', '0004_semester_end_semester_start'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together=set(),
        ),
    ]
