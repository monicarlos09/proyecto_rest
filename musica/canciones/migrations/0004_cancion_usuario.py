# Generated by Django 3.2.5 on 2021-07-09 09:46
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("canciones", "0003_auto_20210708_1051"),
    ]

    operations = [
        migrations.AddField(
            model_name="cancion",
            name="usuario",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="auth.user"
            ),
            preserve_default=False,
        ),
    ]