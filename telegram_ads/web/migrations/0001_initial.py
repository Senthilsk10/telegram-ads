# Generated by Django 5.0 on 2023-12-27 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("client", "0004_file_forwarded_count_alter_client_client_key_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Analytics",
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
                ("total_file_sent", models.IntegerField(blank=True, default=0)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analytics_referenced_client",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Link_to_file",
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
                ("user_chat_id", models.IntegerField(blank=True)),
                (
                    "param",
                    models.CharField(
                        default="K5kOLeHrkIpx5eg-",
                        editable=False,
                        max_length=24,
                        unique=True,
                    ),
                ),
                ("is_shared", models.BooleanField(blank=True, default=False)),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="File_info",
                        to="client.file",
                    ),
                ),
                (
                    "group_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_details",
                        to="client.verified_groups",
                    ),
                ),
            ],
        ),
    ]