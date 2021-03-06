# Generated by Django 2.0.6 on 2018-06-19 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Decomposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DecompositionConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DecompositionSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decomposition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recommender.Decomposition')),
                ('decomposition_configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.DecompositionConfiguration')),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('mpd_set_dir_path', models.CharField(max_length=200)),
                ('challenge_set_dir_path', models.CharField(max_length=200)),
                ('recommendation_dir_path', models.CharField(max_length=200)),
                ('columns_dir_path', models.CharField(max_length=200)),
                ('decomposition_alg_dir_path', models.CharField(max_length=200)),
                ('ml_alg_dir_path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PreparationSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('init_slices', models.IntegerField()),
                ('init_pids', models.IntegerField()),
                ('decomposition_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.DecompositionSession')),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recommender.Environment')),
            ],
        ),
    ]
