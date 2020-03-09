# Generated by Django 2.2.11 on 2020-03-05 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mercury', '0008_auto_20200225_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=40, unique=True)),
                ('event_date', models.DateTimeField()),
                ('event_loc_lat', models.FloatField(blank=True, default=0)),
                ('event_loc_lon', models.FloatField(blank=True, default=0)),
                ('event_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(primary_key=True, serialize=False)),
                ('sensor_name', models.CharField(max_length=40, unique=True)),
                ('sensor_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_id', models.IntegerField(unique=True)),
                ('field_name', models.CharField(max_length=40)),
                ('sensor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_field', to='mercury.Sensor')),
            ],
            options={
                'unique_together': {('field_id', 'sensor_id')},
            },
        ),
        migrations.CreateModel(
            name='General_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stored_at_time', models.DateTimeField()),
                ('data_value', models.FloatField(default=0)),
                ('event_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event_data', to='mercury.Events')),
                ('field_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='field_data', to='mercury.Field', to_field='field_id')),
                ('sensor_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_data', to='mercury.Sensor')),
            ],
            options={
                'unique_together': {('event_id', 'sensor_id', 'field_id')},
            },
        ),
    ]
