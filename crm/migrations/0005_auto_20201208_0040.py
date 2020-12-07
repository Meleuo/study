# Generated by Django 3.1.4 on 2020-12-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20201208_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='class_type',
            field=models.CharField(choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], default='qq', max_length=64, verbose_name='班级类型'),
        ),
    ]
