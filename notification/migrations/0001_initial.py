# Generated by Django 5.1.7 on 2025-03-29 22:24

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0003_remove_post_updated_at_comment_flagged_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ViolationNotification',
            fields=[
                ('notification_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='post.comment')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='post.post')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notification',
                'ordering': ['-created_at'],
            },
        ),
    ]
