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
    path('aesthetic/viewWhyAestheticsk/',viewWhyAestheticsk,name="viewWhyAestheticsk"),
    path('aesthetic/addWhyAestheticsk/',addWhyAestheticsk),
    path('aesthetic/updateWhyAestheticsk/<int:pk>',updateWhyAestheticsk),
    path('aesthetic/delWhyAestheticsk/<int:pk>',delWhyAestheticsk),
    path('aesthetic/viewSpecialized/',viewSpecialized,name="viewSpecialized"),
    path('aesthetic/addSpecialized/',addSpecialized),
    path('aesthetic/updateSpecialized/<int:pk>',updateSpecialized),
    path('aesthetic/delSpecialized/<int:pk>',delSpecialized),
    path('aesthetic/viewService/',viewService,name="viewService"),
    path('aesthetic/updateService/<int:pk>',updateService),
    path('aesthetic/addService/',addService),
    path('aesthetic/delService/<int:pk>',delService),
    path('aesthetic/updateContact/',updateContact),
    path('aesthetic/updateDesigner/',updateDesigner),
    # path('aesthetic/addDesigner/',addDesigner),
    # path('aesthetic/delDesigner/<int:pk>',delDesigner),
    # path('aesthetic/viewDesigners/',viewDesigners),
    path('aesthetic/viewBookedSessions/',viewBookedSessions),
    path('aesthetic/viewBookedDesigns/',viewBookedDesigns),
    path('aesthetic/viewRooms/',viewRooms),
    path('aesthetic/addRoom/',addRoom),
    path('aesthetic/viewRoomImages/<int:pk>',viewRoomImage,name="viewRoomImage"),
    path('aesthetic/addRoomImage/',addRoomImage),
    path('aesthetic/delRoom/<int:pk>',delRoom),
    path('aesthetic/delRoomImage/<int:pk>',delRoomImage),
    path('aesthetic/delBookedDesign/<int:pk>',delBookedDesign),
    path('aesthetic/delBookedSession/<int:pk>',delBookedSession),
    path('aesthetic/error',errorPage,name="error"),
    path('search',searchPage,name="searchResults"),
    path('commingsoon/',commingSoonPage,name="commingsoon"),

    


]
