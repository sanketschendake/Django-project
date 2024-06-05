from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home_url'),
    path('genqr/', views.generate_qr),
    path('fetch_external_data/', views.fetch_external_data),
]
