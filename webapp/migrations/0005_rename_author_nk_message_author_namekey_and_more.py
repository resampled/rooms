# Generated by Django 5.1 on 2025-01-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_room_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='author_nk',
            new_name='author_namekey',
        ),
        migrations.AlterField(
            model_name='message',
            name='author_ip',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
