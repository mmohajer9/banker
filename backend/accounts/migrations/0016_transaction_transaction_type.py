# Generated by Django 3.2.5 on 2021-07-10 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_joinedrequest_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')], default='deposit', max_length=100, verbose_name='Transaction Type'),
        ),
    ]
