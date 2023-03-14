# Generated by Django 3.2.11 on 2022-01-12 21:01

import django.core.serializers.json
import django.db.models.deletion
from cms.utils.compat import DJANGO_3_1
from django.db import migrations, models

import djangocms_frontend.fields

if DJANGO_3_1:
    from django_jsonfield_backport.models import JSONField
else:
    JSONField = models.JSONField


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cms", "0022_auto_20180620_1551"),
    ]

    operations = [
        migrations.CreateModel(
            name="FrontendUIItem",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="%(app_label)s_%(class)s",
                        serialize=False,
                        to="cms.cmsplugin",
                    ),
                ),
                ("ui_item", models.CharField(max_length=30)),
                (
                    "tag_type",
                    djangocms_frontend.fields.TagTypeField(
                        blank=True,
                        default="div",
                        help_text="Select the HTML tag to be used.",
                        max_length=255,
                        verbose_name="Tag type",
                    ),
                ),
                (
                    "config",
                    JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
            ],
            options={
                "verbose_name": "UI item",
            },
            bases=("cms.cmsplugin",),
        ),
    ]
