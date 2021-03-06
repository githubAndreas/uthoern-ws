# Generated by Django 2.0.6 on 2018-06-24 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20180619_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preparation_Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('init_slices', models.IntegerField()),
                ('init_pids', models.IntegerField()),
                ('decomposition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recommender.Decomposition')),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recommender.Environment')),
            ],
        ),
        migrations.RemoveField(
            model_name='decompositionsession',
            name='decomposition',
        ),
        migrations.RemoveField(
            model_name='decompositionsession',
            name='decomposition_configuration',
        ),
        migrations.RemoveField(
            model_name='preparationsession',
            name='decomposition_session',
        ),
        migrations.RemoveField(
            model_name='preparationsession',
            name='environment',
        ),
        migrations.DeleteModel(
            name='DecompositionConfiguration',
        ),
        migrations.DeleteModel(
            name='DecompositionSession',
        ),
        migrations.DeleteModel(
            name='PreparationSession',
        ),
    ]
