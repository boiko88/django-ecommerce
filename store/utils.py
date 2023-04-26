import json
from . models import *

def cookieCart(request):
    # We use try except here because a new user doesn't have 'cart' since it's his first visit 
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    # Here we have to assign get_cart_total and get_cart_items to zero, otherwise 
    # if a user is not logged in we will have an error
    order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    
    for i in cart:
        # We use a try except method here because of {product = Product.objects.get(id=i)}. Sometimes when a new element is deleted via admin panel it can cause an error
        try:
            actualQauntity = cart[i]['quantity']
            cartItems += actualQauntity
            
            product = Product.objects.get(id=i)
            total = (product.price * actualQauntity)
            
            order['get_cart_total'] += total
            order['get_cart_items'] += actualQauntity
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,  
                    },
                'quantity':actualQauntity,
                'get_total':total,
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    
    return {'cartItems':cartItems, 'order':order, 'items':items}