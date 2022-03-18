from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import shutil
from project.apps.api.util import StorageHandler
from .models import TFModel

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def get_model_response(request, model_id):
    tf_model = None
    try:
        tf_model = TFModel.objects.get(id=model_id)
    except:
        return HttpResponse("Model not found!")
    
    model_dir = StorageHandler.download_and_extract(tf_model.model_storage.storage_id)
    
    model = tf.keras.models.load_model(model_dir)
    label_map_file = StorageHandler.read_file(tf_model.label_map_storage.storage_id).decode("utf-8")
    label_map = label_map_file.split(",")
    
    image = tf.keras.preprocessing.image.load_img("test.jpg")
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([tf.image.resize(input_arr, (300,300)).numpy()])

    predictions = model.predict(input_arr)
    max_index = np.argmax(predictions)

    shutil.rmtree(model_dir)

    return HttpResponse(label_map[max_index])

