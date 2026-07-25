from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product

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