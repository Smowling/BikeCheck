# Generated by Django 5.0 on 2024-01-03 13:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0002_adress_store_adress_user"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Adress",
            new_name="Address",
        ),
    ]
