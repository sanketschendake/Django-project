from django.urls import path
from .views import login_view, logout_view,signup_view

urlpatterns = [
    path('lv/', login_view, name='login_url'),
    path('lg/', logout_view, name='logout_url'),
    path('sn/', signup_view, name='signup_url')
]