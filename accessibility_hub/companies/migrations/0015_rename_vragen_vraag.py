# Generated by Django 5.0.2 on 2024-03-09 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_rename_vraag_vragen_vraagtitel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vragen',
            new_name='Vraag',
        ),
    ]
