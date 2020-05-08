from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from product.models import Product, Cart

# Create your views here.


def login(request):
    print('login page!!!!!!!!!')

    if request.user.is_authenticated:
        print('Already logged in')
        products = Product.objects.all()

        current_user = request.user
        carts = Cart.objects.filter(user_id=current_user)

        return render(request,'home.html', {'products' : products, "lenCart":len(carts)})
    else:
        return render(request, 'login.html')


def login_form(request):
    print("login_form")
    if request.method == 'POST':

        username = request.POST['inputEmail']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        # if '@' in username:
        #     kwargs = {'email': username}
        # else:
        #     kwargs = {'username': username}

        # try:
        #     user = get_user_model().objects.get(**kwargs)

        #     if user.check_password(password):

        #         print('user : ', user)
        #         return redirect('/')

        # except User.DoesNotExist:
        #     print('noneee')
        #     return redirect('login')

        products = Product.objects.all()

        if user is not None:
            auth.login(request, user)
            print('valid', username)

            current_user = request.user
            carts = Cart.objects.filter(user_id=current_user)
            return render(request,'home.html', {'products' : products, "lenCart":len(carts)})
        else:
            print('not valid with username : ', username)
            print('trying with email')
            user_name = get_user(username)          
            print("user_name , ", user_name)

            if username.__contains__('@'):
                if user_name.check_password(raw_password=password):
                    print('User found with email, ', username)
                    user = auth.authenticate(username=user_name, password=password)
                    print(user.first_name)
                    auth.login(request, user)
                    current_user = request.user
                    carts = Cart.objects.filter(user_id=current_user)
                    return render(request,'home.html', {'products' : products, "lenCart":len(carts)})
            messages.info(request, 'Invalid credentials, please try again')
            return redirect('login')
    else:
        print("not post")
    return render(request, 'home.html')


def get_user(username):

    try:
        return User.objects.get(email=username)
    except User.DoesNotExist:
        return None

def logout(request):  
    print('logout success')
      
    auth.logout(request)
    return redirect('/')

def register(request):
    print('inside register')

    if request.user.is_authenticated:
        print('Already logged in')
        return redirect('home')

    if request.method == 'POST':
        print("post")
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        username = request.POST['username'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        email = request.POST['email'].strip()

        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        print("user.firstName : ", user.first_name)

        if len(first_name) <= 0 or len(last_name) <= 0 or len(email) <= 0 or len(username) <= 0:
            if len(first_name) <= 0:
                messages.info(request, 'First name should not empty')
            if len(last_name) <= 0:
                messages.info(request, 'Last name should not empty')
            if len(email) <= 0:
                messages.info(request, 'Email should not empty')
            if len(username) <= 0:
                messages.info(request, 'Username should not empty')

            return render(request, 'register.html', {'user': user})

        print('password : ', password1)

        if len(password1) > 0 and len(password2) > 0 and password1 == password2:
            user.password = password1
            if User.objects.filter(username=username).exists():
                print(" username taken")
                messages.info(request, 'Username Taken')
                return render(request, 'register.html', {'user': user})
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Already registered email id')
                return render(request, 'register.html', {'user': user})
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name.upper(), last_name=last_name)
                user.save()
                print('User created')   
                return redirect('login') 

            return render(request, 'register.html', {'user': user})
        else:
            messages.info(request, 'Password not matching')
            return render(request, 'register.html', {'user': user})       
    else:    
        return render(request, 'register.html')
