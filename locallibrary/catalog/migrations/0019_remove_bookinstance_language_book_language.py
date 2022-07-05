# Generated by Django 4.0.6 on 2022-07-05 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_bookinstance_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='language',
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]