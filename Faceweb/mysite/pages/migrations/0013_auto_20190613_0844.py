# Generated by Django 2.2.1 on 2019-06-13 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_auto_20190610_0136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='lesson_1',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='lesson_2',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='lesson_3',
        ),
    ]