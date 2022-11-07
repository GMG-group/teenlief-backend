# Generated by Django 3.2.14 on 2022-11-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_certificatecode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificatecode',
            old_name='expired_date',
            new_name='expire_date',
        ),
        migrations.AddField(
            model_name='certificatecode',
            name='phone',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
