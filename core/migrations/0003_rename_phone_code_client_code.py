# Generated by Django 4.1.4 on 2022-12-15 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_message_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='phone_code',
            new_name='code',
        ),
    ]
