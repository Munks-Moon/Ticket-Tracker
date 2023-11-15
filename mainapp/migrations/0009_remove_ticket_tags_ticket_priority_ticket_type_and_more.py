# Generated by Django 4.2.2 on 2023-07-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_alter_ticket_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='tags',
        ),
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Low', 'Low')], default='Low', max_length=10),
        ),
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('Bug', 'Bug'), ('Feature', 'Feature'), ('Modify', 'Modify')], default='Bug', max_length=10),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Complete', 'Complete')], default='Active', max_length=10),
        ),
    ]