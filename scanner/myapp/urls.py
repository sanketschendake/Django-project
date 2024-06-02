from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('home/', views.home),
    path('genqr/', views.generate_qr),
    path('fetch_external_data', views.fetch_external_data),
]
