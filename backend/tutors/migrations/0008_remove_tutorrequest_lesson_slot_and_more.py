# Generated by Django 4.2.3 on 2023-08-02 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0007_tutoruser_slots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorrequest',
            name='lesson_slot',
        ),
        migrations.RemoveField(
            model_name='tutoruser',
            name='slots',
        ),
        migrations.DeleteModel(
            name='LessonSlot',
        ),
    ]