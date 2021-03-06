# Generated by Django 3.0 on 2020-01-14 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAuthenticationAirrohr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.CharField(max_length=255, verbose_name='Sensor ID (by Airrohr)')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ProjectDevice', verbose_name='Device')),
            ],
        ),
    ]
