from django.contrib import admin
from .models import ModelOutputType, StorageType, Storage, TFModel

admin.site.register(ModelOutputType)
admin.site.register(StorageType)
admin.site.register(Storage)
admin.site.register(TFModel)