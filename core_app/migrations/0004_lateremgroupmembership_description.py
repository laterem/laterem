# Generated by Django 4.1.3 on 2022-12-23 01:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core_app", "0003_lateremcategory_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lateremgroupmembership",
            name="description",
            field=models.TextField(default="", max_length=526),
            preserve_default=False,
        ),
    ]
