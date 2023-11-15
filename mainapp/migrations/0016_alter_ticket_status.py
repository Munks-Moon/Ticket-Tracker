# Generated by Django 4.2.2 on 2023-07-20 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_alter_ticket_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Complete', 'Complete'), ('Backlog', 'Backlog')], default='Backlog', max_length=10),
        ),
    ]