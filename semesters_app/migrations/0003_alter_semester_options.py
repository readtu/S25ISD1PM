# Generated by Django 5.1.4 on 2025-02-20 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('semesters_app', '0002_alter_semester_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semester',
            options={'get_latest_by': ('-year', '-term'), 'ordering': ('-year', '-term')},
        ),
    ]
