# def: views.view()
# class: views.view.as_view()
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_test, name='base_test'),
    path('<slug:room>/', views.room, name='room'),
    path('<slug:room>/enter', views.enter_room, name='enter_room'),
    path('=/create', views.create_room, name='create_room'),
]
