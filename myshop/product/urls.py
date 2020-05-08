from django.urls import path
from . import views

urlpatterns = [
    path('addToCart/addToCart', views.addToCartForm, name='addToCartForm'),
    path('showProduct/addToCart', views.addToCartForm, name='showProductaddToCartForm'),
    path('cart', views.showCart, name='cart'),
    path('updateCart', views.updateCart, name="updateCart"),
    path('deleteRecord', views.deleteRecord, name='deleteRecord')
]
