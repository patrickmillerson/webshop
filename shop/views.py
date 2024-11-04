from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, RequestToBuyForm, CustomLoginForm
from .models import Product, UserProfile
from django.views import View
import random
from django.conf import settings
from .forms import ProductForm

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('product_list')

    return render(request, 'shop/delete_account.html')

@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.userprofile

    if request.method == 'POST':
        # Update user fields
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user_profile.mobile_phone = request.POST['mobile_phone']
        
        user.save()  # Save the user instance
        user_profile.save()  # Save the user profile instance
        
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'shop/edit_profile.html', {'user': user, 'user_profile': user_profile})

@login_required
def profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    return render(request, 'shop/profile.html', {"user": user, "user_profile" : user_profile})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'shop/register.html', {'form': form, 'captcha_value': form.captcha_value})

    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
        else:
            form.add_error(None, "Invalid username or password. Please try again.")
    else:
        form = CustomLoginForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required(login_url='/login/')
def request_to_buy(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        user = request.user
        user_profile = user.userprofile
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
            
            email_message = (
                f"New Purchase Request:\n\n"
                f"Name: {name}\n"
                f"Email: {product.user.email}\n"
                f"Phone: {user_profile.mobile_phone}\n\n"
                f"Product Requested: {product.name}\n"
                f"Product ID: {product.id}\n\n"
                f"Message from the Buyer:\n{message}\n\n"
                f"Please review and respond to this request at your earliest convenience."
            )
            recipient_list = [product.user.email]  # Replace this with the actual seller's email

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
    products = list(Product.objects.all())  # Convert the queryset to a list
    random.shuffle(products)  # Shuffle the list in place
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
    