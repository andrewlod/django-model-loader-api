# Generated by Django 4.0.3 on 2022-03-12 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_storage_type_id_storage_storage_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfmodel',
            name='label_map_storage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tf_model_label_map_storage', to='api.storage'),
        ),
    ]