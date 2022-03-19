import base64
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO
from .models import TFModel
from .forms import UploadImageForm
from project.apps.api.util import StorageHandler
from project.apps.api.util.ModelCache import ModelCache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

def _build_model_response(result, success=True):
    return {
        "success": success,
        "result": result
    }


def _handle_output(tf_model, predictions):
    if tf_model.output_type.type == "String":
        label_map_file = StorageHandler.read_file(tf_model.label_map_storage.storage_id).decode("utf-8")
        label_map = label_map_file.split(",")

        max_index = np.argmax(predictions)

        return label_map[max_index]
    elif tf_model.output_type.type == "Image": #NOT TESTED
        out_image = Image.fromarray(predictions)
        buffered = BytesIO()
        out_image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue())
        return base64_image


@api_view(['POST'])
def get_model_response(request, model_id):
    form = UploadImageForm(request.POST, request.FILES)
    if form.is_valid():
        tf_model = None
        try:
            tf_model = TFModel.objects.get(id=model_id)
        except:
            return Response(_build_model_response("Model not found!", success=False), status=status.HTTP_404_NOT_FOUND)
            
        model = ModelCache.get_model(model_id, tf_model.model_storage.storage_id)
        config = model.get_config()
        input_shape = config["layers"][0]["config"]["batch_input_shape"]
            
        image = Image.open(form.files["image"].open().file)
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([tf.image.resize(input_arr, (input_shape[1], input_shape[2])).numpy()])

        predictions = model.predict(input_arr)

        result = _handle_output(tf_model, predictions)
        return Response(_build_model_response(result))

    
    return Response(_build_model_response("Invalid form!", success=False), status=status.HTTP_400_BAD_REQUEST)

