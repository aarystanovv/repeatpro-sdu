# Generated by Django 4.2.3 on 2023-08-01 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0006_remove_lessonslot_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutoruser',
            name='slots',
            field=models.ManyToManyField(to='tutors.lessonslot'),
        ),
    ]
