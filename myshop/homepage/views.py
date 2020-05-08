from django.shortcuts import render
from django.urls import path
from product.models import Product, Cart

# Create your views here.


def homepage(request):
    
    products = Product.objects.all()
    carts = []
    if request.user.is_authenticated:
        current_user = request.user
        carts = Cart.objects.filter(user_id=current_user)

    return render(request,'home.html', {'products' : products, "lenCart":len(carts)})
