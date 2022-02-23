from django.urls import path
from . import views

urlpatterns = [

    path("get_all/", views.menu_list),
    path("get_all/<int:pk>",views.customer_by_key),
    path("get_allOrders/", views.order_list),
    path("get_allOrders/<int:pk>/", views.order_by_key),

]
