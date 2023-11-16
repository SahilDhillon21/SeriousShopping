# Generated by Django 4.2.3 on 2023-08-29 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_review_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviewImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.review')),
            ],
        ),
        migrations.DeleteModel(
            name='Files',
        ),
    ]