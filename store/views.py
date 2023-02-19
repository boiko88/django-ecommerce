from django.shortcuts import render, redirect
from .models import *


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        # Here we have to assign get_cart_total and get_cart_items to zero, otherwise 
        # if a user is not legged in we will have an error
        order = {'get_cart_total':0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        # Here we have to assign get_cart_total and get_cart_items to zero, otherwise 
        # if a user is not legged in we will have an error
        order = {'get_cart_total':0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)