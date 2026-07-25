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

@login_required
def deliver_order_view(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home')

    if order.status != Order.Status.SHIPPING:
        messages.error(request, "You can only mark shipping orders as delivered.")
        return redirect('home')

    order.status = Order.Status.DELIVERED
    order.save()

    messages.success(request, "Order marked as delivered successfully.")
    return redirect('/dashboard/admin/?section=order-fulfillment')

@login_required
def complete_order_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home')

    if order.status != Order.Status.DELIVERED:
        messages.error(request, "You can only mark delivered orders as completed.")
        return redirect('home')

    order.status = Order.Status.COMPLETED
    order.save()

    messages.success(request, "Order marked as completed successfully.")
    return redirect('/dashboard/?section=pending-orders')

@login_required
def cancel_order_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home')

    if order.status in [Order.Status.COMPLETED, Order.Status.CANCELLED]:
        messages.error(request, "You cannot cancel completed or already cancelled orders.")
        return redirect('home')

    order.status = Order.Status.CANCELLED
    
    for item in order.items.all():
        product = item.product
        product.stock += item.quantity
        product.save()
    
    order.save()

    messages.success(request, "Order cancelled successfully.")
    return redirect('/dashboard/?section=pending-orders')