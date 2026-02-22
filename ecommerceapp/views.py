from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .inherit import Cart_data
from django.contrib.auth.decorators import login_required

def index(request):
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products})
@login_required(login_url='login')
def cart(request):
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    try:
        cart = json.loads(request.COOKIES[cart])
    except:
        cart = {}
    for i in cart:
        cart_items += cart[i]['quantity']
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])
        order['get_cart_total'] += total
        item = {
            'product' : {
                'id' : product.id,
                'name' : product.name,
                'price' : product.price,  
                'image' : product.image,  
            },
            'quantity' : cart[i]['quantity'],
            'get_total' : total
        }
        items.append(item)
    return render(request, 'cart.html', {'items' : items, 'order' : order, 'cart_items' : cart_items})
@login_required(login_url='login')
def checkout(request):
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    total = order.get_cart_total
    if request.method == 'POST':
        address = request.post['address'],
        city = request.post['city'],
        state = request.post['state'],
        zipcode = request.post['zipcode'],
        phone_number = request.post['phone_number'],
        payment = request.post['payment'],
        date_added = request.post['date_added'],
        order = request.post['order'],
        customer = request.post['customer'],
        total_amount = request.post['total_amount'],
        shipping_address = Checkout_details.objects.create(address = address, city = city, state = state, zipcode = zipcode, phone_number = phone_number, payment = payment, date_added = date_added, customer = customer, order = order, total_amount = total_amount)
        if total == order.get_cart_total:
            order.save()
            id = order.id
            alert = True
            return render(request, 'checkout.html',{'alert':alert, 'id':id})
    return render(request, 'checkout.html',{'items' : items, 'order' : order, 'cart_items' : cart_items})
@login_required(login_url='login')
def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    customer = request.user.customer()
    product = Product.objects.get(id = product_id)
    order,created = Order.objects.get_or_create(customer = customer, complete = False)
    order_item,created = Order_item.objects.get_or_create(order = order, product = product)
    update_order,created = Update_order.objects.get_or_create(order_id = order, desc = "Your order has been placed!")
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    order_item.save()
    update_order.save()
    if order_item.quantity <= 0:
        order_item.delete()
    cart_items = order.get_cart_items()
    return JsonResponse({'Message':'Item was updated!','cart_items':cart_items})

def product_view(request, my_id):
    product = Product.objects.filter(id = my_id).first()
    feature = Feature.objects.filter(product = product)
    reviews = Review.objects.filter(product = product)
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    if request.method == 'POST':
        content = request.POST['content']
        customer = request.user.customer()
        review = Review(customer = customer, content = content, product = product)
        review.save()
        return redirect('product_view')
    return render(request,'product_view.html', {'product':product, 'cart_items':cart_items})
def search(request):
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']                                        
    search = request.POST['search']
    products = Product.objects.filter(name=search)
    if request.method == "POST":
        search = request.POST["search"]
        product = Product.objects.filter(name_contains = search)
        return render(request, "search.html", {'search':search, 'products':products, 'cart_items':cart_items})
    else:
        return render(request, 'search.html')
    
def change_password(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                return render(request, 'change_password.html')
            else:
                return render(request, 'change_password.html', {'current_password':current_password,'new_password':new_password})
        except:
            pass
    return render(request, 'change_password.html',)

def contact(request):
    if request.method == 'POST':
        name = request.post.get('name')
        email = request.post.get('email')
        phone = request.post.get('phone')
        contact = Contact(name='name',email='email',phone='phone')
        contact.save()
        alert = True
        return render(request, 'contact.html',{'alert':alert})
    return render(request, 'contact.html')

def tracker(request):
    if not request.User.is_authenticated:
        return redirect('/login')
    data = Cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    if request.method =='POST':
        order_id = request.post.get('order_id')
        order = Order.objects.filter(id = order_id).first()
        order_items = Order_item.objects.filter(order = order)
        update_order = Update_order.objects.filter(order_id = order_id)
        return render(request, 'tracker.html',{'order_id':order_id,'order':order,'order_items':order_items,'update_order':update_order})
def Login(request):
    if request.method == 'POST':
        username = request.post.get('username')
        password = request.post.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
           login(request, user)
        else:
            messages.error(request, 'Invalid username or passord!')
            return redirect(request, 'login.html')
    return redirect(request, 'login,html')

def Logout(request):
    logout(request)
    messages.succes(request, 'Logged out successfully')
    return redirect(request, 'login.html')
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        number = request.POST.get('phone_number')
        confirm_password = request.POST.get('password2')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        if password!=confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')
        user = User.objects.create_user(username=username,password=password,email=email,number=number,full_name=full_name)
        user.save()
        return render(request, 'login.html')
    return render(request, 'register.html')