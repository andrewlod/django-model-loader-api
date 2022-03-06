from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os

# Create your views here.
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