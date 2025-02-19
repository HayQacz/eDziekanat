# Generated by Django 4.2.19 on 2025-02-08 21:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_customuser_semester_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='day_of_week',
        ),
        migrations.AddField(
            model_name='lesson',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='Data zajęć'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='semester',
            field=models.PositiveIntegerField(help_text='Aktualny semestr (np. 1, 2, 3, ...)'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='semester_group',
            field=models.CharField(default=20, help_text='Dwucyfrowy kod grupy (np. 10, 21)', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='group',
            field=models.CharField(help_text='Grupa, dwucyfrowy kod', max_length=2),
        ),
    ]
