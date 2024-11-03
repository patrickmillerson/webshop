from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, RequestToBuyForm, CustomLoginForm
from .models import Product
from django.views import View
from django.conf import settings
from .forms import ProductForm

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.email = request.POST['email']
        user.save()
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'shop/edit_profile.html', {'user': user})

@login_required
def profile_view(request):
    return render(request, 'shop/profile.html')  # Make sure to create this template

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')  # Redirect to your desired URL
    else:
        form = CustomLoginForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required(login_url='/login/')
def request_to_buy(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = RequestToBuyForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Log to console or send an email
            print(f"Request to buy {product.name} from {name} ({email}): {message}")
            # You can send an email notification here if needed
            # Prepare the email
            subject = f'Request to Buy {product.name}'
            email_message = f"{name} wants to buy {product.name} with ID#: {product.id}.\n\nMessage: {message}"
            recipient_list = [settings.DEFAULT_SELLER_EMAIL]  # Replace this with the actual seller's email

            # Send email (this will be the placeholder email for now)
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            return redirect('product_list')  # Redirect to the product list after submission
    else:
        form = RequestToBuyForm()

    return render(request, 'shop/request_to_buy.html', {'form': form, 'product': product})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Set the user to the logged-in user
            product.save()
            return redirect('product_list')  # Redirect to the product list after saving
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'shop/product_detail.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.user:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('product_list')  # Redirect to the product list or wherever you want

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_list')

    return render(request, 'shop/delete_product_confirm.html', {'product': product})
    