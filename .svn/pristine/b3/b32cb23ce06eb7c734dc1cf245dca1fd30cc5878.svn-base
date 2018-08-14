from django.urls import path
from . import views
from .views import CoincideImages, GetCorrectImage, GetTemplate

urlpatterns = [
    path('', views.index, name='home'),
    path('resize/', views.resize,name='resize'),
    path('areaOfShape/', views.areaOfShape,name='areaOfShape'),
    path('coincide-images/', CoincideImages.as_view(), name='Coincide_Images'),
    path('ajax/get-correct-image/', GetCorrectImage, name='Get_Correct_Image'),
    path('ajax/get-template/', GetTemplate, name='Get_Template'),
]
