from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import Product

@login_required
def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    
    category = request.GET.get('category')
    size = request.GET.get('size')
    price_range = request.GET.get('price_range')
    sort = request.GET.get('sort')
    q = request.GET.get('q')
    
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(brand__icontains=q) | Q(category__icontains=q)
        )
    if category:
        products = products.filter(category=category)
    if size:
        products = products.filter(size=size)
    if price_range:
        if price_range == '0-499':
            products = products.filter(price__gte=0, price__lte=499)
        elif price_range == '500-999':
            products = products.filter(price__gte=500, price__lte=999)
        elif price_range == '1000-4999':
            products = products.filter(price__gte=1000, price__lte=4999)
        elif price_range == '5000-9999':
            products = products.filter(price__gte=5000, price__lte=9999)
        elif price_range == '10000-49999':
            products = products.filter(price__gte=10000, price__lte=49999)
        elif price_range == '50000-99999':
            products = products.filter(price__gte=50000, price__lte=99999)
        elif price_range == '100000':
            products = products.filter(price__gte=100000)
            
    if sort:
        if sort == 'oldest':
            products = products.order_by('created_at')
        elif sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'stock_asc':
            products = products.order_by('stock')
        elif sort == 'stock_desc':
            products = products.order_by('-stock')
            
    return render(request, 'main/products_page.html', {'products': products})

@login_required
def add_product_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to add products.")
        return redirect('home')

    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand', 'NepFit')
        category = request.POST.get('category')
        size = request.POST.get('size')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_image = request.FILES.get('product_image')
        is_active = request.POST.get('is_active') == 'true'

        if not name:
            errors['name'] = "Product name is required."
        if not brand:
            errors['brand'] = "Brand name is required."
        if not category:
            errors['category'] = "Product category is required."
        if not size:
            errors['size'] = "Product size is required."
        if not description:
            errors['description'] = "Product description is required."
        if not price:
            errors['price'] = "Product price is required."
        if not stock:
            errors['stock'] = "Product stock quantity is required."
        if not product_image:
            errors['product_image'] = "Product image is required."
        
        if errors:
            return render(request, 'main/add_product_page.html', {'errors': errors, 'data': request.POST})
        
        product = Product(
            name=name,
            brand=brand,
            category=category,
            size=size,
            description=description,
            price=price,
            stock=stock,
            product_image=product_image,
            is_active=is_active
        )
        product.save()
        messages.success(request, f"Product '{product.name}' added successfully.")
        return redirect('/dashboard/admin/?section=product-management')

    return render(request, 'main/add_product_page.html')

@login_required
def edit_product_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to edit products.")
        return redirect('home')

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('/dashboard/admin/?section=product-management')

    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand', 'NepFit')
        category = request.POST.get('category')
        size = request.POST.get('size')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_image = request.FILES.get('product_image')
        is_active = request.POST.get('is_active') == 'true'
        
        if not name:
            errors['name'] = "Product name is required."
        if not brand:
            errors['brand'] = "Brand name is required."
        if not category:
            errors['category'] = "Product category is required."
        if not size:
            errors['size'] = "Product size is required."
        if not description:
            errors['description'] = "Product description is required."
        if not price:
            errors['price'] = "Product price is required."
        if not stock:
            errors['stock'] = "Product stock quantity is required."            

        if errors:
            return render(request, 'main/edit_product_page.html', {'errors': errors, 'data': request.POST, 'product': product})

        product.name = name
        product.brand = brand
        product.category = category
        product.size = size
        product.description = description
        product.price = price
        product.stock = stock
        product.is_active = is_active
        if product_image:
            product.product_image = product_image 
        product.save()
        
        messages.success(request, f"Product '{product.name}' updated successfully.")
        return redirect('/dashboard/admin/?section=product-management')

    return render(request, 'main/edit_product_page.html', {'product': product})

@login_required
def delete_product_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to delete products.")
        return redirect('home')

    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")

    return redirect('/dashboard/admin/?section=product-management')

@login_required
def is_active_toggle_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to change product status.")
        return redirect('home')

    try:
        product = Product.objects.get(id=product_id)
        product.is_active = not product.is_active
        product.save()
        status = "activated" if product.is_active else "deactivated"
        messages.success(request, f"Product '{product.name}' has been {status}.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")

    return redirect('/dashboard/admin/?section=product-management')

@login_required
def product_detail_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('products')

    return render(request, 'main/product_detail_page.html', {'product': product})