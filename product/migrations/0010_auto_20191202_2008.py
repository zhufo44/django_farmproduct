# Generated by Django 2.2.1 on 2019-12-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20191202_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='people',
            field=models.CharField(default='', max_length=30, verbose_name='联系人'),
        ),
        migrations.AddField(
            model_name='storage',
            name='phone',
            field=models.CharField(default='', max_length=30, verbose_name='联系电话'),
        ),
    ]