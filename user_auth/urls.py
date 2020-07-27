from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('password_reset/', views.reset_password, name='reset_password'),

]
