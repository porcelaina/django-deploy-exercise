from django.urls import path, include
from basic_app5 import views

# Template URLs!
app_name='basic_app5'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]