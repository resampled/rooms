# Generated by Django 5.1.5 on 2025-01-30 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_message_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='banned_nk',
            field=models.TextField(max_length=9000, null=True),
        ),
    ]
