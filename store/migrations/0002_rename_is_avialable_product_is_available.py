# Generated by Django 5.0.2 on 2024-03-18 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_avialable',
            new_name='is_available',
        ),
    ]
