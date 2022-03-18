from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
import numpy as np
from PIL import Image
from project.apps.api.util import StorageHandler
from project.apps.api.util.ModelCache import ModelCache
from .models import TFModel
from .forms import UploadImageForm

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def get_model_response(request, model_id):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            tf_model = None
            try:
                tf_model = TFModel.objects.get(id=model_id)
            except:
                return HttpResponse("Model not found!")
            
            model = ModelCache.get_model(model_id, tf_model.model_storage.storage_id)
            config = model.get_config()
            input_shape = config["layers"][0]["config"]["batch_input_shape"]

            label_map_file = StorageHandler.read_file(tf_model.label_map_storage.storage_id).decode("utf-8")
            label_map = label_map_file.split(",")
            
            image = Image.open(form.files["image"].open().file)
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([tf.image.resize(input_arr, (input_shape[1], input_shape[2])).numpy()])

            predictions = model.predict(input_arr)
            max_index = np.argmax(predictions)

            return HttpResponse(label_map[max_index])
    
    return HttpResponse("Method not allowed")

