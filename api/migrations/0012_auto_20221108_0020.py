# Generated by Django 3.2.14 on 2022-11-07 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_certificatecode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatecode',
            name='code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='certificatecode',
            name='status',
            field=models.CharField(max_length=2),
        ),
    ]
