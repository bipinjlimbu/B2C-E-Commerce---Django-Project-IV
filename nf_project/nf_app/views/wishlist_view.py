from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Wishlist, Product

@login_required
def wishlist_view(request):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access the wishlist.")
        return redirect('home')
    
    wishlist_items = Wishlist.objects.filter(customer=request.user).select_related('product')
    return render(request, 'main/wishlist_page.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_toggle_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.user.is_staff:
        messages.error(request, "You are not authorized to modify the wishlist.")
        return redirect('home')
    
    if product.stock <= 0:
        messages.error(request, "This product is out of stock and cannot be added to the wishlist.")
        return redirect(f'/products/{product_id}/')
    
    wishlist_item, created = Wishlist.objects.get_or_create(customer=request.user, product=product)

    if not created:
        wishlist_item.delete()
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        messages.success(request, f"{product.name} added to your wishlist.")

    return redirect(f'/products/{product_id}/')

@login_required
def wishlist_remove_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to modify the wishlist.")
        return redirect('home')
    
    try:
        wishlist_item = Wishlist.objects.get(customer=request.user, product_id=product_id)
        wishlist_item.delete()
        messages.success(request, "Item removed from your wishlist.")
    except Wishlist.DoesNotExist:
        messages.error(request, "Item not found in your wishlist.")

    return redirect('wishlist')