# Generated by Django 5.1.5 on 2025-01-24 23:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_alter_studentclass_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentclass',
            unique_together={('user', 'course_number', 'section_number')},
        ),
    ]
