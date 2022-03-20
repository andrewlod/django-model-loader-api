from django.test import TestCase, Client
from django.contrib.admin.sites import AdminSite
from project.apps.api.admin import ImageModelFormAdmin
from project.apps.api.models import ModelOutputType, TFModel, StorageType, Storage
from django.core.files.uploadedfile import SimpleUploadedFile
import time

class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


class TFModelTestCase(TestCase):
    def setUp(self):
        model_output_types = ["String", "Image"]
        storage_types = ["AWS", "Local"]
        for type in model_output_types:
            ModelOutputType.objects.create(type=type)
    
        for type in storage_types:
            StorageType.objects.create(type=type)


    def create_tf_model(self):
        request = MockRequest()
        request.user = MockSuperUser()
        request.data = {
            "model_output_type": "String",
            "model_storage_type": "AWS",
            "model_name": "test_string_model"
        }
        request.files = {
            "model": SimpleUploadedFile("model", open("project/tests/tf_model/data/test_model.zip", "rb").read(), content_type="application/zip"),
            "model_label_map": SimpleUploadedFile("model_label_map", open("project/tests/tf_model/data/test_label_map.txt", "rb").read(), content_type="text/plain"),
        }
        request.POST = request.data
        request.FILES = request.files
        request.method = "POST"


        ma = ImageModelFormAdmin(TFModel, AdminSite())
        ma.save_model(obj=TFModel(), request=request, form=None, change=None)
        

    def predict_tf_model(self):
        c = Client()
        response = c.post("/api/predict/test_string_model/", {"image": open("project/tests/tf_model/data/test_image.jpg", "rb")})
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content["success"], True)
        self.assertEqual(content["result"], "Tomato Healthy")


    def test_sequentially(self):
        self.create_tf_model()
        self.predict_tf_model()