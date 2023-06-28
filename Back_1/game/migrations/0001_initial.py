# Generated by Django 3.2.19 on 2023-06-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('font', models.CharField(max_length=30, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='game')),
            ],
        ),
        migrations.CreateModel(
            name='Predict_Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=30, null=True)),
                ('stage', models.CharField(max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=500, null=True)),
                ('score', models.FloatField()),
                ('is_correct', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SentenceContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sentence', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SyllableContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('syllable', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
