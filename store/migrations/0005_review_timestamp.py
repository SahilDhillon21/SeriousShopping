# Generated by Django 4.2.3 on 2023-08-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_customer_email_alter_customer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
