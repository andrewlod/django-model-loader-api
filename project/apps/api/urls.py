from django.urls import path
from . import views

urlpatterns = [
    path("<str:model_id>/", views.get_model_response),
    path("register/string/", views.register_str_model),
    path("register/image/", views.register_image_model)
]