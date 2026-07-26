from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Review, Product

@login_required
def add_review_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to add reviews.")
        return redirect('home')
    
    product = Product.objects.get(id=product_id)
    if not product:
        messages.error(request, "Product not found.")
        return redirect('products')
    
    if Review.objects.filter(product=product, customer=request.user).exists():
        messages.error(request, "You have already reviewed this product.")
        return redirect(f'/products/{product_id}/')
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        
        if not rating:
            errors['rating'] = "Rating is required."
        if not comment:
            errors['comment'] = "Comment is required."
        
        if errors:
            return render(request, 'main/add_review_page.html', {'product': product, 'errors': errors})
        
        review = Review(
            product=product,
            customer=request.user,
            rating=rating,
            comment=comment
        )
        review.save()
        messages.success(request, "Your review has been added successfully.")
        return redirect(f'/products/{product_id}/')
        
    return render(request, 'main/add_review_page.html', {'product': product})