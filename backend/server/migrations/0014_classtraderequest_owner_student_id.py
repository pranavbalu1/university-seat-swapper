# Generated by Django 5.1.5 on 2025-01-29 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_remove_classtraderequest_downvotes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classtraderequest',
            name='owner_student_id',
            field=models.CharField(default='-1', max_length=20),
        ),
    ]
