# Generated by Django 3.2.21 on 2023-10-12 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SpaceAPI",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("space_is_open", models.BooleanField(default=False)),
                (
                    "space_message",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("status_last_change", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SpaceAPISensor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sensor_type",
                    models.CharField(
                        choices=[
                            ("temperature", "Temperature"),
                            ("barometer", "Barometer"),
                            ("radiation", "Radiation"),
                            ("humidity", "Humidity"),
                            ("beverage_supply", "Beverage Supply"),
                            ("power_consumption", "Power Consumption"),
                            ("wind", "Wind Data"),
                            ("network_connections", "Network Connections"),
                            ("account_balance", "Account Balance"),
                            ("network_traffic", "Network Traffic"),
                        ],
                        max_length=100,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("value", models.DecimalField(decimal_places=3, max_digits=10)),
                ("unit", models.CharField(max_length=50)),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpaceAPISensorProperties",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("value", models.DecimalField(decimal_places=3, max_digits=10)),
                ("unit", models.CharField(max_length=100)),
                (
                    "sensor_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to="api_spacedirectory.spaceapisensor",
                    ),
                ),
            ],
        ),
    ]