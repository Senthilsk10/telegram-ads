# Generated by Django 5.0 on 2023-12-27 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0005_alter_client_client_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="client_key",
            field=models.CharField(
                default="fbGjtunmcfaqjwc3shTMO6N56jlROFmz",
                editable=False,
                max_length=24,
                unique=True,
            ),
        ),
    ]
