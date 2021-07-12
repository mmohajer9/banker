# Generated by Django 3.2.5 on 2021-07-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_transaction_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(blank=True, max_length=50, null=True, verbose_name='Action')),
                ('path', models.CharField(blank=True, max_length=50, null=True, verbose_name='Path')),
                ('method', models.CharField(blank=True, max_length=50, null=True, verbose_name='Method')),
                ('user', models.CharField(blank=True, max_length=50, null=True, verbose_name='User')),
                ('remote_address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Remote Address')),
                ('content_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Content-Type')),
                ('log_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Log Name')),
                ('browser', models.CharField(blank=True, max_length=50, null=True, verbose_name='Browser')),
                ('user_agent', models.CharField(blank=True, max_length=50, null=True, verbose_name='User Agent')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'AuditLog',
                'verbose_name_plural': 'AuditLogs',
            },
        ),
    ]
