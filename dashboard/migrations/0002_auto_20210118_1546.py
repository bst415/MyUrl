# Generated by Django 3.1.5 on 2021-01-18 10:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_urls',
            name='url_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_urls',
            name='short_char',
            field=models.CharField(blank=True, max_length=8),
        ),
    ]