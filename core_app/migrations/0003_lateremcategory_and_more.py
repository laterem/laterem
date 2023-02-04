# Generated by Django 4.1.4 on 2022-12-22 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core_app", "0002_lateremuser_lateremassignment_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LateremCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("root_category", models.IntegerField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="lateremworkcategory",
            name="root_category",
        ),
        migrations.AddField(
            model_name="lateremgroup",
            name="can_manage_tasks",
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name="LateremCategoryCategory",
        ),
        migrations.AlterField(
            model_name="lateremwork",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core_app.lateremcategory",
            ),
        ),
        migrations.DeleteModel(
            name="LateremWorkCategory",
        ),
    ]
