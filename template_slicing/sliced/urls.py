from django.urls import path
from . import views

urlpatterns = [
    path('home',views.index,name="home"),
    path('',views.login_view,name="login"),
    path('logout',views.logout_view,name="logouts"),
    path('addservices', views.add_service, name='add_services' ),
    path('allServices',views.allServices,name="allServices"),
    path('edittables/<int:id>',views.edittables,name="edittables"),
    path('deletetables/<int:id>',views.deletetables,name="deletetables"),
    path('subServices',views.addsubServices,name="subServices"),
    path('allsubServices',views.allsubServices,name="allsubServices"),
    path('editSubService/<int:id>',views.editSubService,name="editSubService"),
    path('deleteSubService/<int:id>',views.deleteSubService,name="deleteSubService"),
    path('allBooking', views.allOrders, name = 'allBooking'),
    path('updateOrder/<int:id>/<str:type>', views.updateOrder, name='updateOrder')
]