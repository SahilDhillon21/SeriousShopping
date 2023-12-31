# Generated by Django 4.2.3 on 2023-08-30 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_reviewimages_delete_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer'),
        ),
    ]
