# Generated by Django 4.1.3 on 2023-03-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0006_laterembugreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laterembugreport',
            name='attachment',
        ),
        migrations.AlterField(
            model_name='laterembugreport',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
