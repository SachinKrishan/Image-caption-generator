from django.urls import path
from . import views

#URL config
urlpatterns = [
    path('generate_caption/', views.caption_generation_view, name='generate_caption')
]