from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'), 
    path('crimemap/', views.crimemap_view, name='crimemap'),
    
]