# Generated by Django 5.0.1 on 2024-02-18 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_alter_income_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='source',
            field=models.CharField(choices=[('0', 'Lương'), ('1', 'Kinh Doanh'), ('2', 'Phụ Thu Nhập'), ('3', 'Khác')], max_length=100),
        ),
    ]
