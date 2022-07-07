from django.urls import path

from app.views import *

urlpatterns = [
    path('', home,name='homepage'),
    path('rooms/<int:pk>',room,name='room'),
    path('bookSession/',bookSession),
    path('bookDesign/<int:pk>',bookDesign),
    path('aesthetic/adminArea/',adminPage,name="adminArea"),
    path('aesthetic/updateAbout/',updateAbout),
]
