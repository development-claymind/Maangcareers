# Generated by Django 5.0 on 2024-01-25 08:35

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('caption', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('discount_percentage', models.SmallIntegerField()),
                ('archive', models.BooleanField(default=False)),
                ('popular', models.BooleanField(default=False)),
                ('premium', models.BooleanField(default=False)),
                ('pre_recorded', models.BooleanField(default=False)),
                ('lectures', models.SmallIntegerField()),
                ('class_duration', models.CharField(help_text='please input here in format: hh:mm', max_length=5)),
                ('course_duration', models.SmallIntegerField()),
                ('projects', models.SmallIntegerField()),
                ('mobile_computer', models.BooleanField(default=True)),
                ('certificate', models.BooleanField(default=True)),
                ('short_description', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('author_name', models.CharField(max_length=50)),
                ('author_message', models.TextField(blank=True, null=True)),
                ('author_photo', models.ImageField(default='default.png', upload_to='course_author_photos')),
                ('thumbnail', models.FileField(upload_to='course_thumbnails')),
                ('demo_video', models.URLField(blank=True, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_participants', models.SmallIntegerField(default=30)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='batches', to='userManagement.instructor')),
            ],
            options={
                'verbose_name_plural': 'batches',
            },
        ),
        migrations.CreateModel(
            name='BatchJoined',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=50, null=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined', to='courseManagement.batch')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined', to='userManagement.student')),
                ('assign_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courseManagement.projectname')),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='batches', through='courseManagement.BatchJoined', to='userManagement.student'),
        ),
        migrations.AddField(
            model_name='batch',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='courseManagement.course'),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('week', models.CharField(choices=[('1', 'Week 1'), ('2', 'Week 2'), ('3', 'Week 3'), ('4', 'Week 4'), ('5', 'Week 5'), ('6', 'Week 6'), ('7', 'Week 7'), ('8', 'Week 8')], max_length=1)),
                ('file', models.FileField(upload_to='course_notes')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseManagement.course')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_topic', models.TextField(blank=True, null=True)),
                ('project_name', models.ManyToManyField(help_text='After each eg press enter twice to create new project', to='courseManagement.projectname')),
            ],
        ),
        migrations.AddField(
            model_name='batchjoined',
            name='assign_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courseManagement.projecttopic'),
        ),
        migrations.AddField(
            model_name='batch',
            name='project_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courseManagement.projecttopic'),
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=128, null=True)),
                ('start_time', models.TimeField()),
                ('start_date', models.DateField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('week', models.CharField(blank=True, choices=[('1', 'Week 1'), ('2', 'Week 2'), ('3', 'Week 3'), ('4', 'Week 4'), ('5', 'Week 5'), ('6', 'Week 6'), ('7', 'Week 7'), ('8', 'Week 8')], max_length=1, null=True)),
                ('day', models.CharField(blank=True, choices=[('1', 'Day 1'), ('2', 'Day 2'), ('3', 'Day 3')], max_length=1, null=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='courseManagement.batch')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Week number or Week Name', max_length=50)),
                ('week', models.IntegerField(blank=True, null=True)),
                ('lock', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabi', to='courseManagement.course')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('duration', models.DurationField(blank=True, choices=[(datetime.timedelta(seconds=1800), '30 min'), (datetime.timedelta(seconds=3600), '1 Hr'), (datetime.timedelta(seconds=5400), '1 Hr 30 min'), (datetime.timedelta(seconds=7200), '2 Hr'), (datetime.timedelta(seconds=9000), '2 Hr 30 min'), (datetime.timedelta(seconds=10800), '3 Hr')], null=True)),
                ('day', models.CharField(blank=True, choices=[('1', 'Day 1'), ('2', 'Day 2'), ('3', 'Day 3')], max_length=1, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courseManagement.week')),
            ],
        ),
    ]
