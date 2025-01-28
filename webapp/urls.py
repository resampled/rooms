# def: views.view()
# class: views.view.as_view()
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:room>/', views.room, name='room'),
    path('<slug:room>/editcode', views.edit_room_editcode, name='edit_room_editcode'),
    path('<slug:room>/enter', views.enter_room, name='enter_room'),
    path('=/create', views.create_room, name='create_room'),
]
