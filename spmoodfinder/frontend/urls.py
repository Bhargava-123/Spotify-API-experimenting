from django.urls import path,include
from . import views

urlpatterns = [
    path('mostplayed/',views.mostPlayedView)
]