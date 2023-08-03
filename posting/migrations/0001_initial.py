# Generated by Django 4.2.3 on 2023-08-01 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.BigAutoField(help_text='Comment ID', primary_key=True, serialize=False)),
                ('context', models.TextField(max_length=2000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('feed_id', models.BigAutoField(help_text='Feed ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('context', models.TextField(max_length=2000, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField()),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
            options={
                'db_table': 'Feed',
            },
        ),
        migrations.CreateModel(
            name='Feed_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='media/posting/default_image.jpeg', null=True, upload_to='posting')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.feed')),
            ],
            options={
                'db_table': 'Feed_image',
            },
        ),
        migrations.CreateModel(
            name='Comment_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='media/posting/default_image.jpeg', null=True, upload_to='posting')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.comment')),
            ],
            options={
                'db_table': 'Comment_image',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.feed'),
        ),
    ]
