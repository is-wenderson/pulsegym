from django.urls import path
from .views import evo_webhook, tv_dashboard_api

urlpatterns = [
    path('webhook/', evo_webhook, name='evo_webhook'),
    path('tv/', tv_dashboard_api, name='tv_dashboard_api'),
]