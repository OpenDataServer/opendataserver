# Generated by Django 3.0 on 2019-12-31 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAuthenticationTTN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=255, verbose_name='Application ID (by TTN)')),
                ('access_key', models.CharField(max_length=255, verbose_name='Access key (by TTN)')),
                ('discovery_address', models.CharField(default='discovery.thethings.network:1900', max_length=255)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ProjectDevice', verbose_name='Device')),
            ],
        ),
    ]