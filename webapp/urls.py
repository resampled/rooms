# def: views.view()
# class: views.view.as_view()
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_test, name='base_test'),
]