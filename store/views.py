from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CommentForm


def store(request):
    # Get cart data using the cartData function
    data = cartData(request)
    # Get the number of cart items from the cart data
    cartItems = data['cartItems']
    products = Product.objects.all()

    context = {
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)


def faq(request):
    # Get cart data using the cartData function
    data = cartData(request)
    # Get the number of cart items from the cart data
    cartItems = data['cartItems']
    products = Product.objects.all()

    context = {
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'store/faq.html', context)


def cart(request):
    # Get cart data using the cartData function
    data = cartData(request)
    # Get the number of cart items from the cart data
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    # Get cart data using the cartData function
    data = cartData(request)
    # Get the number of cart items from the cart data
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    # Load the JSON data from the request body
    data = json.loads(request.body)
    # Get the product ID and action from the JSON data
    productId = data['productId']
    action = data['action']
    # Print the action and product ID for debugging purposes
    print('Action:', action)
    print('Product:', productId)

    # Get the customer associated with the request user
    customer = request.user.customer
    # Get the product with the given ID
    product = Product.objects.get(id=productId)
    # Get or create an order for the customer with complete=False
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    # Get or create an order item for the order and product
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    # Update the order item quantity based on the action
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    # Delete the order item if the quantity is zero or less
    if orderItem.quantity <= 0:
        orderItem.delete()

    # Return a JSON response indicating success
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    # Print the request body for debugging purposes
    print('Data:', request.body)
    # Generate a unique transaction ID using the current timestamp
    transaction_id = datetime.datetime.now().timestamp()
    # Parse the request body as JSON
    data = json.loads(request.body)

    if request.user.is_authenticated:
        # If the user is authenticated, associate the order with the customer
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        # If the user is not authenticated, create a guest order
        customer, order = guestOrder(request, data)

    # Calculate the total amount from the form data
    total = float(data['form']['total'])
    # Set the transaction ID for the order
    order.transaction_id = transaction_id


    # Check if the total amount matches the order's cart total
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        # If the order has a shipping address, create a new ShippingAddress object
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    # Return a JSON response indicating that the payment is complete
    return JsonResponse('Payment Complete', safe=False)


def loginRegistration(request):
    if request.method == 'POST':
        # Get the username and password from the POST data
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            # Try to get a user with the given username
            user = User.objects.get(username=username)
        except:
            # If the user doesn't exist, show an error message
            messages.error(request, 'User does not exist')

        # Authenticate the user with the given username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated, log them in and redirect to the store page
            login(request, user)
            return redirect('store')
        else:
            # If the user is not authenticated, show an error message
            messages.error(request, 'Username OR password does not exist')

    # If the request method is not POST, create an empty context dictionary
    context = {}

    return render(request, 'store/login_registration.html', context)


def userRegistration(request):
    # Create an instance for the current form
    form = UserCreationForm()

    if request.method == 'POST':
        # Bind the form to the POST data
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create a new user object from the form data convert it to lowercase and save
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # create a new customer object and associate it with the user
            customer = Customer.objects.create(user=user)
            customer.name = user.username
            customer.email = user.email
            customer.save()
            # automatically assign a user to a group - in this case user so he can't see some pages
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            login(request, user)
            return redirect('store')

        else:
            messages.error(
                request, 'Ooops, something went wrong during the registration')

    context = {
        'form': form,
    }

    return render(request, 'store/user_registration.html', context)


def changePassword(request):
    # Create a PasswordChangeForm instance for the current user
    form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        # Bind the form to the submitted data
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Save the new password and update the user's session authentication hash
            print('Form is valid')
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('store')
        else:
            # print errors if the form is not valid
            print('Form is not valid')
            print(form.errors)

    context = {
        'form': form,
    }

    return render(request, 'store/change_password.html', context)




def logoutUser(request):
    logout(request)
    return redirect('store')


def description(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'store/description.html', context)


def createComment(request):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
        
    context = {
        'form': form,
    }
    
    return render(request, 'store/comment_form.html', context) 