# Generated by Django 2.0.6 on 2018-06-28 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0008_prediction_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction_session',
            name='num_batch_size',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
