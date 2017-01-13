# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-05 00:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20161204_1927'),
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Time', models.TimeField()),
                ('Purpose', models.TextField(max_length=250)),
                ('Doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Appointments', to='accounts.Doctor')),
                ('Hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Hospital')),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Appointments', to='accounts.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject', models.CharField(max_length=100)),
                ('Text', models.TextField(max_length=500)),
                ('Date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Viewed', models.BooleanField(default=False)),
                ('Receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receiver', to=settings.AUTH_USER_MODEL)),
                ('Sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]