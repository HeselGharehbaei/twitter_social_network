# Generated by Django 4.2.2 on 2023-06-19 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_like'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='Post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='posts',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
