# Generated by Django 4.0 on 2022-07-04 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_rename_grade_student_grade'),
        ('Quiz', '0007_remove_answer_answer_question_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Accounts.student'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='particpations',
            field=models.ManyToManyField(null=True, to='Accounts.Student'),
        ),
    ]
