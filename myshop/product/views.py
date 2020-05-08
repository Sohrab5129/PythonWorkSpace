from django.shortcuts import render, redirect
from product.models import Product, Cart, ShowCart, Quantity
from django.contrib.auth.models import User, auth
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers

# Create your views here.


def show(request, id):

    print(request.META['PATH_INFO'])
    # print(request.META['HTTP_HOST'])
    # print(request.META['QUERY_STRING'])

    # FULL_URL_WITH_QUERY_STRINg = request.build_absolute_uri()
    # FULL_URL = request.build_absolute_uri('?')
    # ABSOLUTE_ROOT = request.build_absolute_uri('/')[:-1].strip("/")
    # ABSOLUTE_ROOT_URL =  request.build_absolute_uri('/').strip("/")

    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        current_user = request.user
        carts = Cart.objects.filter(user_id=current_user)
        return render(request, 'showProductDetails.html', {'product': product, "lenCart": len(carts)})
    else:
        return redirect('login')


def addToCart(request, id):
    print('add to cart')

    # qty1 = request.GET['qty']
    # print(qty1)
    if request.user.is_authenticated:

        print('Already logged in')
        product = Product.objects.get(id=id)
        current_user = request.user

        # print(f"product id = {id}")
        # print(f"user id = {current_user.id}")
        # print(f"unit price = {product.price}")

        status = saveCart(current_user, product, 1)

        current_user = request.user
        carts = Cart.objects.filter(user_id=current_user)

        if status:
            return render(request, 'showProductDetails.html', {'product': product, 'message': 'Added successfully to Cart', "lenCart": len(carts)})
        else:
            return render(request, 'showProductDetails.html', {'product': product, 'message': 'Already Added', "lenCart": len(carts)})

    else:
        return redirect('login')


def saveCart(current_user, product, qty):
    print("save cart")
    carts = Cart.objects.filter(user_id=current_user, product_id=product)
    if not carts:
        cart = Cart()
        cart.product_id = product
        cart.user_id = current_user
        cart.qty = qty
        cart.price = product.price

        quantity = Quantity.objects.filter(product_id=product)

        # update quantity
        for q in quantity:
            q.soldQty = q.soldQty + qty
            q.qty = q.qty - qty

            if q.qty >= 0:
                q.save()
            else:
                return False

        # update product availability
        quantity = Quantity.objects.filter(product_id=product)

        for q in quantity:
            if q.qty == 0:
                product.availability = False
                product.save()

        cart.save()
        return True
    else:
        return False


def addToCartForm(request):
    print("inside add to cart")

    if request.user.is_authenticated and request.method == 'POST':
        print("post")
        product_id = request.POST['product_id'].strip()
        qty = int(request.POST['qty'].strip())
        product = Product.objects.get(id=product_id)

        current_user = request.user
        carts = Cart.objects.filter(user_id=current_user)

        quantity = Quantity.objects.filter(product_id=product)

        for q in quantity:
            if q.qty < qty:
                message = 'Only '+str(q.qty)+' '+product.name+' available'
                return render(request, 'showProductDetails.html', {'product': product, 'message': message})

        if qty <= 0:
            return render(request, 'showProductDetails.html', {'product': product, 'message': 'Please inter valid quantity'})

        current_user = request.user
        status = saveCart(current_user, product, qty)

        if status:
            return render(request, 'showProductDetails.html', {'product': product, 'message': 'Added successfully to Cart', "lenCart": len(carts)})
        else:
            return render(request, 'showProductDetails.html', {'product': product, 'message': 'Already Added', "lenCart": len(carts)})

    else:
        return redirect('login')


def showCart(request):
    print('inside show cart')

    if request.user.is_authenticated:
        current_user = request.user
        carts = Cart.objects.filter(user_id=current_user)
        myCart = []
        sum = 0

        for cart in carts:
            showCart = ShowCart()
            showCart.id = cart.id

            product = Product.objects.get(id=cart.product_id.id)
            showCart.name = product.name
            showCart.qty = cart.qty
            showCart.price = cart.price * showCart.qty
            showCart.img = product.img.url
            showCart.prod_id = product.id
            showCart.unit_price = cart.price
            sum += showCart.price
            myCart.append(showCart)

        return render(request, 'cart.html', {"myCart": myCart, "sum": sum, "lenCart": len(carts)})
    else:
        return redirect('login')


def updateCart(request):

    qty = int(request.GET.get('qty', None))
    product_id = int(request.GET.get('product_id', None))
    message = ''
    current_user = request.user

    carts = Cart.objects.filter(user_id=current_user, product_id=product_id)
    addedQty = 0
    product = Product.objects.get(id=product_id)
    quantity = Quantity.objects.filter(product_id=product)

    for cart in carts:
        if cart and int(qty) > 0:
            addedQty = cart.qty
            cart.qty = qty
            
            # update quantity
            for q in quantity:    
                availableQty = q.qty  
                q.soldQty = q.soldQty + qty - int(addedQty)
                q.qty = q.qty - qty + int(addedQty)

                if q.qty >= 0:
                    q.save()
                    cart.save()
                else:
                    if availableQty == 0:
                        message = 'Sorry, '+product.name+' not available right now'
                    else:
                        message = 'Only '+str(availableQty)+' '+product.name+' available'
                    print(message)
                    data = {
                            'message': message
                    }
                    return JsonResponse(data, safe=False)
                    
            # update product availability
            quantity = Quantity.objects.filter(product_id=product)

            for q in quantity:
                if q.qty == 0:
                    product.availability = False
                else:
                    product.availability = True
                product.save()

    updated_cart = Cart.objects.filter(user_id=current_user)

    data = {
        'message': message
    }

    # data = serializers.serialize("json", updated_cart)

    # print(data)

    return JsonResponse(data, safe=False)


def deleteRecord(request):

    product_id = int(request.GET.get('product_id', None))
    current_user = request.user
    carts = Cart.objects.filter(user_id=current_user, product_id=product_id)
    product = Product.objects.get(id=product_id)
    quantity = Quantity.objects.filter(product_id=product)
    addedProductQty = 0
  
    for cart in carts:
        
        if cart:
            
            addedProductQty = cart.qty

            # update quantity
            for q in quantity:    
                q.qty = q.qty + addedProductQty
                q.soldQty = q.soldQty - addedProductQty
                q.save()

            # update product availability
            quantity = Quantity.objects.filter(product_id=product)

            for q in quantity:
                if q.qty == 0:
                    product.availability = False
                else:
                    product.availability = True
                product.save()
            
            cart.delete()


    data = {
        'status': "Successfully deleted record"
    }
    return JsonResponse(data)
