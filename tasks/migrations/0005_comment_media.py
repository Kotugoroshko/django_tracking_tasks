# Generated by Django 5.1.4 on 2025-01-25 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='comments_media/'),
        ),
    ]
