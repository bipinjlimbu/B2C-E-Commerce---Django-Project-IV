from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Order

@login_required
def dispatch_order_view(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home')

    if order.status != Order.Status.CONFIRMED:
        messages.error(request, "You can only dispatch confirmed orders.")
        return redirect('home')

    order.status = Order.Status.SHIPPING
    order.save()

    messages.success(request, "Order dispatched successfully.")
    return redirect('/dashboard/admin/?section=order-fulfillment')
