from django.urls import path 
from . import views
urlpatterns = [
    path('', views.product_list, name='product_list' ),
    path('product_list_ajax/', views.product_list_ajax, name='product_list_ajax' ),
    
    path('product/<int:id>/', views.product_details, name='product_details' ),
]