from django.urls import path

from app.views import *

urlpatterns = [
    path('', home,name='homepage'),
    path('rooms/<int:pk>',room,name='room'),
    path('bookSession/',bookSession),
    path('bookDesign/<int:pk>',bookDesign),
    path('aesthetic/adminArea/',adminPage,name="adminArea"),
    path('aesthetic/updateAbout/',updateAbout),
    path('aesthetic/updateWhyAestheticsk/',updateWhyAestheticsk),
    path('aesthetic/updateSpecialized/',updateSpecialized),
    path('aesthetic/updateService/',updateService),
    path('aesthetic/updateContact/',updateContact),
    path('aesthetic/updateDesigner/',updateDesigner),
    path('aesthetic/viewBookedSessions/',viewBookedSessions),
    path('aesthetic/viewBookedDesigns/',viewBookedDesigns),
    path('aesthetic/viewRooms/',viewRooms),
    path('aesthetic/addRoom/',addRoom),
    path('aesthetic/delRoom/<int:pk>',delRoom),

]
