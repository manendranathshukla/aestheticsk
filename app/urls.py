from django.urls import path

from app.views import *

urlpatterns = [
    path('', home,name='homepage'),
    path('rooms/<int:pk>',room,name='room'),
    path('bookSession/',bookSession),
    path('bookDesign/<int:pk>',bookDesign),
    path('aesthetic/login/',loginPage,name='login'),
    path('aesthetic/register/',registerPage,name='signup'),
    path('aesthetic/logout/',Logout,name='logout'),
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
    path('aesthetic/viewRoomImages/<int:pk>',viewRoomImage,name="viewRoomImage"),
    path('aesthetic/delRoom/<int:pk>',delRoom),
    path('aesthetic/delBookedDesign/<int:pk>',delBookedDesign),
    path('aesthetic/delBookedSession/<int:pk>',delBookedSession),
    path('aesthetic/error',errorPage,name="error"),
    


]
