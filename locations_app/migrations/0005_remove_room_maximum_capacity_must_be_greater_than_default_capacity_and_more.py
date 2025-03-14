# Generated by Django 5.1.4 on 2025-02-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations_app', '0004_room_maximum_capacity_must_be_greater_than_default_capacity'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='room',
            name='maximum_capacity_must_be_greater_than_default_capacity',
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.CheckConstraint(condition=models.Q(('maximum_capacity__gte', models.F('default_capacity'))), name='maximum_capacity_must_be_greater_than_default_capacity', violation_error_message='The maximum_capacity of a Room must be greater than or equal to its default_capacity.'),
        ),
    ]
