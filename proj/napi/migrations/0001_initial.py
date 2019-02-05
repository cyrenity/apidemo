# Generated by Django 2.1.5 on 2019-02-05 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessQueueAction',
            fields=[
                ('tracking_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('phone', models.BigIntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('trans', 'Transgender/Other')], max_length=10)),
                ('type', models.CharField(choices=[('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3')], max_length=10)),
                ('remarks', models.TextField(max_length=100)),
                ('citizen_number', models.CharField(max_length=15)),
                ('created', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('task_id', models.CharField(max_length=100)),
                ('tracking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='napi.ProcessQueueAction')),
            ],
        ),
    ]
