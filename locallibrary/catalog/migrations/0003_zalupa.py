# Generated by Django 4.0.5 on 2022-06-23 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_author_book_bookinstance_genre_delete_mymodelname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zalupa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zalupa_name', models.CharField(max_length=100)),
                ('pizda_name', models.CharField(max_length=100)),
                ('huy_name', models.DateField(blank=True, null=True)),
                ('beath_name', models.DateField(blank=True, null=True, verbose_name='Govno')),
            ],
        ),
    ]
