from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from ..models import User, Product, Order

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return redirect('home')
    
    section = request.GET.get('section', 'customer-management')
    context = {
        'section': section,
        'awaiting_dispatch_count': Order.objects.filter(status=Order.Status.CONFIRMED).count(),
        'awaiting_delivery_count': Order.objects.filter(status=Order.Status.SHIPPING).count(),
        'delivered_count': Order.objects.filter(status=Order.Status.DELIVERED).count(),
        'completed_count': Order.objects.filter(status=Order.Status.COMPLETED).count(),
        'cancelled_count': Order.objects.filter(status=Order.Status.CANCELLED).count(),
    }
    
    if section == 'customer-management':
        context['customers'] = User.objects.filter(is_staff=False).order_by('-date_joined')
    elif section == 'product-management':
        context['products'] = Product.objects.all().order_by('-created_at')
    elif section == 'order-fulfillment':
        context['orders'] = Order.objects.all().order_by('-created_at')
    elif section == 'product-reviews':
        context['reviews'] = None
    elif section == 'revenue_logs':
        context['revenue_logs'] = None
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access the customer dashboard.")
        return redirect('home')
    
    section = request.GET.get('section', 'pending-orders')
    context = {
        'section': section,
        'gross_spent': Order.objects.filter(customer=request.user, status=Order.Status.COMPLETED).aggregate(total=models.Sum('total_amount'))['total'] or 0,
        'average_spent': Order.objects.filter(customer=request.user, status=Order.Status.COMPLETED).aggregate(avg=models.Avg('total_amount'))['avg'] or 0
    }
    
    if section == 'pending-orders':
        context['pending_orders'] = Order.objects.exclude(customer=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
    elif section == 'my-orders':
        context['orders'] = Order.objects.filter(customer=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
    elif section == 'my-reviews':
        context['reviews'] = None
    elif section == 'total-spent':
        context['total_spent'] = Order.objects.filter(customer=request.user, status=Order.Status.COMPLETED).order_by('-created_at')

    return render(request, 'dashboard/customer_dashboard.html', context)