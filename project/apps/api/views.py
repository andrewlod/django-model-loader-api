from django.shortcuts import render
from django.http import HttpResponse
from .forms import StringModelForm, ImageModelForm
from uuid import uuid4
from .util import StorageHandler
from .models import Storage, TFModel, StorageType, ModelOutputType
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import json


def get_model_response(request, model_id):
    model = tf.keras.Sequential([hub.KerasLayer('https://tfhub.dev/google/aiy/vision/classifier/food_V1/1')])

    label_map = None
    with open("aiy_food_V1_labelmap.txt", "r", encoding="cp850") as file:
        label_map = file.read().split(",")
    
    image = tf.keras.preprocessing.image.load_img("test.jpg")
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([tf.image.resize(input_arr, (192,192)).numpy()])

    predictions = model.predict(input_arr)
    max_index = np.argmax(predictions)

    return HttpResponse(label_map[max_index])

#REMOVE THIS LATER
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_str_model(request):
    if request.method == 'POST':
        form = StringModelForm(request.POST, request.FILES)
        if form.is_valid():
            storage_type = form.data["storage_type"]
            model_name = form.data["model_name"]
            model = form.files["model"]
            label_map = form.files["label_map"]
            
            model_id, storage_type_id = StorageHandler.store_file(model, storage_type)
            label_map_id, _ = StorageHandler.store_file(label_map, storage_type)

            model_storage = Storage(storage=model_id, storage_type=StorageType.objects.get(id=storage_type_id))
            label_map_storage = Storage(storage=label_map_id, storage_type=StorageType.objects.get(id=storage_type_id))
            model_storage.save()
            label_map_storage.save()

            model_data = TFModel(id=model_name, model_storage=model_storage, label_map_storage=label_map_storage, output_type=ModelOutputType.objects.get(type="String"))
            model_data.save()

            return HttpResponse({
                "model_name": model_name,
                "model_id": model_id,
                "label_map_id": label_map_id
            })
            #change HttpResponse to response (install Django Rest Framework)


def register_image_model(request):
    content = json.loads(request.body)["content"]

"""
Str output
{
    model: file
    label_map: file,
    storage_type: str
}
Image output
{
    model: file,
    storage_type: str
}
"""