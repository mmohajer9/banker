# Generated by Django 3.2.5 on 2021-07-09 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.UUIDField(default=198802520769366122566080242665285868009, editable=False, primary_key=True, serialize=False),
        ),
    ]