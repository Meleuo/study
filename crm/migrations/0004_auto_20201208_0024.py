# Generated by Django 3.1.4 on 2020-12-07 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20201208_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='咨询日期'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_consult_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='最后跟进日期'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='next_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='预计再次跟进时间'),
        ),
    ]