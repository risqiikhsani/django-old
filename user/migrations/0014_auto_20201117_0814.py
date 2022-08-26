# Generated by Django 3.1 on 2020-11-17 01:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0013_follow_follower_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follower',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='request',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
