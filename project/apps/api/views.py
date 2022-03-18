from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
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
    
    model_dir = StorageHandler.download_file(tf_model.model_storage.storage_id)
    
    model = tf.keras.models.load_model(model_dir)
    print(list(model.signatures.keys()))

    """
    label_map = None
    with open("aiy_food_V1_labelmap.txt", "r", encoding="cp850") as file:
        label_map = file.read().split(",")
    
    image = tf.keras.preprocessing.image.load_img("test.jpg")
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([tf.image.resize(input_arr, (192,192)).numpy()])

    predictions = model.predict(input_arr)
    max_index = np.argmax(predictions)

    return HttpResponse(label_map[max_index])
    """
    return HttpResponse("test")
