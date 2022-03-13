from django.urls import path
from . import views

urlpatterns = [
    path("predict/<str:model_id>/", views.get_model_response)
]