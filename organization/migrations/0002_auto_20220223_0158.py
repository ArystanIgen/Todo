# Generated by Django 3.1.7 on 2022-02-22 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['created_at'], 'permissions': [('create_task', 'Can create task'), ('read_task', 'Can read task')], 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
    ]