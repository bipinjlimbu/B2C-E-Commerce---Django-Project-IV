from django.shortcuts import render

def home_page(request):
    products = None
    return render(request, 'main/home_page.html', {'products': products})