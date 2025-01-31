# Generated by Django 5.1.5 on 2025-01-28 01:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_delete_requestinteraction'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTradeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Open'), ('accepted', 'Accepted'), ('closed', 'Closed')], default='open', max_length=20)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
                ('favorites', models.ManyToManyField(blank=True, related_name='favorite_requests', to=settings.AUTH_USER_MODEL)),
                ('offered_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offered_class', to='server.studentclass')),
                ('requested_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_class', to='server.studentclass')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trade_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AcceptedRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accepted_requests', to=settings.AUTH_USER_MODEL)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='server.classtraderequest')),
            ],
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]
