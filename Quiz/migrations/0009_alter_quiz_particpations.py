# Generated by Django 4.0 on 2022-07-04 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_rename_grade_student_grade'),
        ('Quiz', '0008_alter_answer_student_alter_quiz_particpations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='particpations',
            field=models.ManyToManyField(blank=True, null=True, to='Accounts.Student'),
        ),
    ]
