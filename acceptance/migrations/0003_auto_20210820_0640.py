# Generated by Django 3.0 on 2021-08-20 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acceptance', '0002_auto_20210819_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sign',
            old_name='brench_id',
            new_name='branch_id',
        ),
    ]
