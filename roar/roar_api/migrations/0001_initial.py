# Generated by Django 4.2.15 on 2024-08-09 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Active_Information",
            fields=[
                (
                    "id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=300)),
                ("discount_info", models.CharField(max_length=200)),
                ("active_description", models.TextField()),
                ("active_promo_image", models.CharField(max_length=500)),
                ("source_web_name", models.CharField(max_length=200)),
                ("webSales", models.CharField(max_length=300)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("comment", models.CharField(max_length=200)),
                ("hitRate", models.IntegerField(default=0)),
            ],
            options={"db_table": "active_info",},
        ),
        migrations.CreateModel(
            name="Active_Show_Information",
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
                ("show_start_time", models.DateTimeField()),
                ("show_end_time", models.DateTimeField()),
                ("show_location", models.CharField(max_length=200)),
                ("show_location_addr", models.CharField(max_length=200)),
                ("on_sale", models.BooleanField(default=False)),
                ("price", models.CharField(max_length=200)),
                (
                    "active_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="roar_api.active_information",
                    ),
                ),
            ],
            options={"db_table": "active_show_info",},
        ),
        migrations.CreateModel(
            name="Active_Category_Unit",
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
                ("category", models.CharField(max_length=100, null=True)),
                ("show_unit", models.CharField(max_length=200, null=True)),
                ("master_unit", models.CharField(max_length=200)),
                ("sub_unit", models.CharField(max_length=200)),
                ("support_unit", models.CharField(max_length=200)),
                ("other_unit", models.CharField(max_length=200)),
                (
                    "active_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="roar_api.active_information",
                    ),
                ),
            ],
            options={"db_table": "active_category_info",},
        ),
    ]