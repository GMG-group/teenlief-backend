# Generated by Django 3.2.14 on 2022-10-18 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_promise_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('explanation', models.TextField()),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='marker',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='marker',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
        migrations.AlterField(
            model_name='promise',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.FloatField()),
                ('todo_review', models.BooleanField(default=True)),
                ('content', models.CharField(max_length=500)),
                ('date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_author', to=settings.AUTH_USER_MODEL)),
                ('helper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_helper', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
