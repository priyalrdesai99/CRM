# Generated by Django 2.1.7 on 2019-04-04 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0004_auto_20190310_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('cost_price', models.CharField(blank=True, max_length=100)),
                ('sell_price', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]
