from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return redirect('home')
    
    section = request.GET.get('section', 'customer-management')
    context = {
        'section': section,
    }
    
    if section == 'customer-management':
        context['customers'] = User.objects.filter(is_staff=False).order_by('-date_joined')
    elif section == 'product-management':
        context['products'] = Product.objects.all().order_by('-created_at')
    elif section == 'order-fulfillment':
        context['orders'] = None
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
    }
    
    if section == 'pending-orders':
        context['pending_orders'] = None
    elif section == 'my-orders':
        context['my_orders'] = None
    elif section == 'my-reviews':
        context['reviews'] = None
    elif section == 'total-spent':
        context['total_spent'] = None

    return render(request, 'dashboard/customer_dashboard.html', context)