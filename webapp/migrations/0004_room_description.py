# Generated by Django 5.1 on 2025-01-20 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_remove_room_owner_nk_room_edit_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.TextField(max_length=1400, null=True),
        ),
    ]
