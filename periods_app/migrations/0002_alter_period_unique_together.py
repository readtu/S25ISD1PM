# Generated by Django 5.1.4 on 2025-02-20 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('periods_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='period',
            unique_together={('year', 'term')},
        ),
    ]
