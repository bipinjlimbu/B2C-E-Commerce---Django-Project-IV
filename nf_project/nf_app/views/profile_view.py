from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User

@login_required
def profile_view(request):
    return render(request, 'main/profile_page.html')

@login_required
def edit_profile_view(request):
    user = User.objects.get(pk=request.user.pk)
    
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if not username:
            errors['username'] = "Username is required."
        elif User.objects.filter(username=username).exclude(pk=user.pk).exists():
            errors['username'] = "Username already exists."
            
        if not email:
            errors['email'] = "Email is required."
        elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
            errors['email'] = "Email already exists."

        if errors:
            return render(request, 'main/edit_profile_page.html', {'errors': errors, 'data': request.POST})

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.address = address
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'main/edit_profile_page.html')

@login_required
def delete_profile_view(request, user_id):
    if request.user.pk != user_id and not request.user.is_staff:
        messages.error(request, "You are not authorized to delete this profile.")
        return redirect('profile')
    
    user = User.objects.get(pk=user_id)
    user.delete()
    messages.success(request, "Profile deleted successfully.")
    
    if request.user.is_staff:
        return redirect('/dashboard/admin/?section=customer-management')
    else:
        return redirect('logout')