# Generated by Django 4.0.6 on 2022-08-21 17:39

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_reader_gender_reader_user_img_alter_reader_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='user_img',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage('/media/userImg'), upload_to=''),
        ),
    ]