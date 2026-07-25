from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Cart, CartItem

@login_required
def add_to_cart_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Staff members cannot add products to the cart.")
        return redirect('home')
    
    product = Product.objects.get(id=product_id)
    
    if product.stock <= 0:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect(f'/products/{product_id}/')
    
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
    if request.user.is_staff:
        messages.error(request, "Staff members cannot access the cart.")
        return redirect('home')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'main/cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def increase_cart_item_quantity(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Staff members cannot modify the cart.")
        return redirect('home')
    
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Quantity of {cart_item.product.name} increased.")
    else:
        messages.error(request, f"Cannot increase quantity. Only {cart_item.product.stock} items in stock.")
    
    return redirect('cart')

@login_required
def decrease_cart_item_quantity(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Staff members cannot modify the cart.")
        return redirect('home')
    
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f"Quantity of {cart_item.product.name} decreased.")
    else:
        messages.error(request, "Quantity cannot be less than 1. To remove the item, please use the remove option.")
    
    return redirect('cart')

@login_required
def remove_cart_item_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Staff members cannot modify the cart.")
        return redirect('home')
    
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    cart_item.delete()
    
    messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
    return redirect('cart')