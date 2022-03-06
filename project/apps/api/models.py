from operator import mod
from django.db import models

class ModelOutputType(models.Model):
    type = models.CharField(max_length=16)

    class Meta:
        db_table = "model_output_type"
    
class StorageType(models.Model):
    type = models.CharField(max_length=16)

    class Meta:
        db_table = "storage_type"

class Storage(models.Model):
    url = models.CharField(max_length=32)
    storage_type_id = models.ForeignKey(StorageType, on_delete=models.CASCADE)

    class Meta:
        db_table = "storage"

class TFModel(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    model_storage_id = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='tf_model_storage')
    label_map_storage_id = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='tf_model_label_map_storage')
    output_type_id = models.ForeignKey(ModelOutputType, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "tf_model"
