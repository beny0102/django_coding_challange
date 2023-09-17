# Generated by Django 3.2 on 2023-09-17 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0002_auto_20220520_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_datetime', models.DateTimeField(auto_now=True)),
                ('reason', models.CharField(max_length=120)),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='licenses.license')),
            ],
        ),
    ]