# Generated by Django 2.0.6 on 2018-06-28 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0007_training_session_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction_Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('export_file_name', models.CharField(max_length=100)),
                ('training_session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recommender.Training_Session')),
            ],
        ),
    ]