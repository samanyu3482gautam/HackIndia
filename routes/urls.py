from django.urls import path
from . import views

urlpatterns = [
    path('find_route/', views.find_shortest_route, name='find_route'),
    path('search_flights/', views.search_flights, name='search_flights'),
    path('payment_page/',views.payment_page,name='payment_page'),
     

]