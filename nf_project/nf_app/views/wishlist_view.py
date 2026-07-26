from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Wishlist, Product

@login_required
def wishlist_toggle_view(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(customer=request.user, product=product)

    if not created:
        wishlist_item.delete()
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        messages.success(request, f"{product.name} added to your wishlist.")

    return redirect(f'/products/{product_id}/')