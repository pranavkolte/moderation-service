# Generated by Django 5.1.7 on 2025-03-29 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='creaeted_at',
            new_name='created_at',
        ),
    ]
