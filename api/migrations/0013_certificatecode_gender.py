# Generated by Django 3.2.14 on 2022-11-07 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20221108_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatecode',
            name='gender',
            field=models.CharField(default='M', max_length=1),
            preserve_default=False,
        ),
    ]
