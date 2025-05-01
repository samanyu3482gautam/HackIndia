from django.urls import path

from . import views 
from .views import *
urlpatterns = [
   path('SignIn/',views.login_page, name='SignIn'),
   path('SignUp/',views.sign_up, name='SignUp')
   
]
