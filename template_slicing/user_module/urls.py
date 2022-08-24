from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('logins',views.login_view,name="logins"),
    path('logout',views.logout_view,name="logout"),
    path('register',views.register_view,name="register"),
    path('subService/<int:id>', views.subService, name = "subService"),
    path('addToCart/<int:subId>', views.addToCart, name='addToCart'),
    path('viewCart', views.viewCart, name='viewCart'),
    path('removeItemCart/<int:id>', views.removeItemCart, name='removeItemCart'),
    path('checkOut', views.checkOut, name='checkOut'),
    path('allOrders', views.allOrders, name='allOrders')
]