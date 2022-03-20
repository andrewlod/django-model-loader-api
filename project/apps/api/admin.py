from django.contrib import admin, messages
from .models import ModelOutputType, StorageType, Storage, TFModel
from .forms import ImageModelForm
from .util import StorageHandler
from uuid import uuid4

admin.site.register(ModelOutputType)
admin.site.register(StorageType)
admin.site.register(Storage)


class ImageModelFormAdmin(admin.ModelAdmin):
    fields = ['model', 'model_output_type', 'model_label_map', 'model_storage_type', 'model_name']
    form = ImageModelForm

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':

            form = ImageModelForm(request.POST, request.FILES)
            if form.is_valid():
                storage_type = form.data["model_storage_type"]
                output_type = form.data["model_output_type"]
                model_name = form.data["model_name"]
                model = form.files["model"]

                try:
                    TFModel.objects.get(id=model_name)
                    messages.error(request, "Model already exists!")
                except:
                    pass
            
                model_id = str(uuid4())

                model_storage = Storage.objects.create(storage_id=model_id, storage_type=StorageType.objects.get(type=storage_type))

                obj.id = model_name
                obj.model_storage = model_storage
                obj.label_map_storage = None
                obj.output_type = ModelOutputType.objects.get(type=output_type)

                if output_type == "String":
                    label_map = form.files["model_label_map"]
                    label_map_id = str(uuid4())
                    label_map_storage = Storage.objects.create(storage_id=label_map_id, storage_type=StorageType.objects.get(type=storage_type))

                    obj.label_map_storage = label_map_storage

                    StorageHandler.store_file(label_map, storage_type, file_id=label_map_id)

                StorageHandler.store_file(model, storage_type, file_id=model_id)
                
                TFModel.objects.create(id=obj.id, model_storage=obj.model_storage, label_map_storage=obj.label_map_storage, output_type=obj.output_type)
        else:
            return ImageModelForm()

admin.site.register(TFModel, ImageModelFormAdmin)