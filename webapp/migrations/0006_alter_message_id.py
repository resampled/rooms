# Generated by Django 5.1 on 2025-01-21 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_rename_author_nk_message_author_namekey_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]