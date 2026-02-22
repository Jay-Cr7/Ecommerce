from .models import *
def Cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order_created = Order.objects.get_or_create(customer = customer, complete = False)
        items = Order.orderitem_set.all()
        cart_items = Order.get_cart_items()
    else:
        items = []
        order = {'get_total':0, 'get_items':0}
        cart_items = order['get_items']
    return{'cart_items':cart_items,'items':items,'order':order}