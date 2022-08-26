# Generated by Django 3.1 on 2020-12-09 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0017_auto_20201208_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='to_user',
        ),
        migrations.AddField(
            model_name='follow',
            name='to_user',
            field=models.ManyToManyField(null=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follower',
            name='from_user',
        ),
        migrations.AddField(
            model_name='follower',
            name='from_user',
            field=models.ManyToManyField(null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follower',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
