# Generated by Django 4.0.5 on 2022-06-23 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_zalupa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassV1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p1', models.CharField(max_length=100, verbose_name='s22')),
                ('p2', models.CharField(max_length=100, verbose_name='S22')),
                ('p3', models.DateField(max_length=100, verbose_name='s33')),
                ('p4', models.DateField(max_length=100, verbose_name='s44')),
            ],
        ),
        migrations.DeleteModel(
            name='Zalupa',
        ),
    ]
