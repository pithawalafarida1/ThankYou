# Generated by Django 3.1.5 on 2021-01-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thankyousys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=122, null=True)),
                ('password', models.CharField(blank=True, max_length=122, null=True)),
                ('email', models.CharField(blank=True, max_length=122, null=True)),
            ],
        ),
    ]
