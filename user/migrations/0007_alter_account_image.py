# Generated by Django 4.2.2 on 2023-06-19 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/photos', verbose_name='Image'),
        ),
    ]
