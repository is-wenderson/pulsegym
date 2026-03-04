from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.evo_webhook, name='evo_webhook'),
]