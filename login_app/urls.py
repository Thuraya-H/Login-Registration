from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('reg', views.register),
    path('log', views.log),
    path('success', views.success),
    path('destroy', views.destroy)
]