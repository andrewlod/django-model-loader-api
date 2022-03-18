from .Singleton import Singleton
from . import StorageHandler
import tensorflow as tf
import shutil

class ModelCache(metaclass=Singleton):
    models = {}
    
    def add_model(key, storage_id):
        model_dir = StorageHandler.download_and_extract(storage_id)
        model = tf.keras.models.load_model(model_dir)

        ModelCache.models[key] = model

        shutil.rmtree(model_dir)

        return model

    def get_model(key, storage_id):
        if key not in ModelCache.models:
            ModelCache.add_model(key, storage_id)
        
        return ModelCache.models[key]