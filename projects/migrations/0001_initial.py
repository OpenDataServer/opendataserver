# Generated by Django 3.0 on 2019-12-22 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Project Name')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('data_source', models.CharField(choices=[('ttn', 'The Things Network'), ('airrohr', 'Airrohr/Luftdaten.info')], max_length=255, verbose_name='Data source')),
                ('geo_lat', models.FloatField(verbose_name='Latitude')),
                ('geo_lon', models.FloatField(verbose_name='Longitude')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('type', models.CharField(max_length=255, verbose_name='Sensor type')),
                ('field_name_in_data', models.CharField(max_length=255, verbose_name='Field name in data')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ProjectDevice', verbose_name='Device')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('member', 'Member'), ('restricted', 'Restricted')], max_length=255, verbose_name='Role')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAuthenticationTTN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=255, verbose_name='Application ID (by TTN)')),
                ('access_key', models.CharField(max_length=255, verbose_name='Access key (by TTN)')),
                ('discovery_address', models.CharField(max_length=255)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ProjectDevice', verbose_name='Device')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAuthenticationAirrohr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.CharField(max_length=255, verbose_name='Application ID (by TTN)')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ProjectDevice', verbose_name='Device')),
            ],
        ),
    ]
