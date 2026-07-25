from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Cart, CartItem

@login_required
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if CartItem.objects.filter(cart__customer=request.user, product=product).exists():
        messages.info(request, f"{product.name} is already in your cart.")
        return redirect(f'/products/{product_id}/')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect(f'/products/{product_id}/')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'main/cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def increase_cart_item_quantity(request, product_id):
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Quantity of {cart_item.product.name} increased.")
    else:
        messages.error(request, f"Cannot increase quantity. Only {cart_item.product.stock} items in stock.")
    
    return redirect('cart')