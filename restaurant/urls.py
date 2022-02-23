from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="restaurant"),
    path("<int:id>", views.restaurant_detail.as_view(), name="detail_restaurant"),
    path("get_all/", views.restaurant_res),
    path("get_all/<int:pk>",views.restaurant_res_by_key),
]
