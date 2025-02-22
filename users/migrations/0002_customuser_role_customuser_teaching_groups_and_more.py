# Generated by Django 5.1.6 on 2025-02-22 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('dydaktyk', 'Dydaktyk'), ('administrator', 'Administrator')], default='student', max_length=15),
        ),
        migrations.AddField(
            model_name='customuser',
            name='teaching_groups',
            field=models.CharField(blank=True, help_text='Lista grup, w których nauczasz (oddzielone przecinkami)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='index_number',
            field=models.CharField(blank=True, help_text='np. AB12345', max_length=7, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='semester',
            field=models.PositiveIntegerField(blank=True, default=1, help_text='Aktualny semestr (np. 1, 2, 3, ...)', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='semester_group',
            field=models.CharField(blank=True, help_text='Dwucyfrowy kod grupy (np. 10, 21)', max_length=2, null=True),
        ),
    ]
