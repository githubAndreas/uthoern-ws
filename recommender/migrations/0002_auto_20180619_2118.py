# Generated by Django 2.0.6 on 2018-06-19 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='environment',
            old_name='mpd_set_dir_path',
            new_name='mdp_set_dir_path',
        ),
    ]
