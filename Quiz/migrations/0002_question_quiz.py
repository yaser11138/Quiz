# Generated by Django 4.0 on 2022-07-02 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Quiz.quiz'),
        ),
    ]