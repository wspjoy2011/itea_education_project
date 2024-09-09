# Generated by Django 5.1 on 2024-09-09 18:17

import django.db.models.deletion
import django_extensions.db.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=['name'])),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=['name'])),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=['name'])),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=['name'])),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('year', models.IntegerField()),
                ('time', models.IntegerField()),
                ('imdb', models.FloatField()),
                ('votes', models.IntegerField()),
                ('meta_score', models.FloatField(blank=True, null=True)),
                ('gross', models.FloatField(blank=True, null=True)),
                ('description', models.TextField()),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=['name'])),
                ('certification', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movies', to='movies.certification')),
            ],
            options={
                'ordering': ('name', 'year'),
            },
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='director_movies', to='movies.director')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_directors', to='movies.movie')),
            ],
            options={
                'unique_together': {('movie', 'director')},
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_movies', to='movies.genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_genres', to='movies.movie')),
            ],
            options={
                'unique_together': {('movie', 'genre')},
            },
        ),
        migrations.CreateModel(
            name='MovieStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_stars', to='movies.movie')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star_movies', to='movies.star')),
            ],
            options={
                'unique_together': {('movie', 'star')},
            },
        ),
    ]
