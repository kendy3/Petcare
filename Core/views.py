from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignUpForm, RescueRequestForm, BookingForm, AdoptionRequestForm
from .models import UserProfile, RescueRequest, AdoptableAnimal, Product, ServicePlan, Booking, Order

def home(request):
    return render(request, 'core/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number')
            )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def rescue_request_view(request):
    if request.method == 'POST':
        form = RescueRequestForm(request.POST, request.FILES)
        if form.is_valid():
            rescue_request = form.save(commit=False)
            rescue_request.user = request.user
            rescue_request.save()
            messages.success(request, 'Rescue request submitted successfully! Check your email for confirmation.')
            return redirect('rescue_request')
    else:
        form = RescueRequestForm()
    return render(request, 'core/rescue_request.html', {'form': form})

def adoptions_view(request):
    animals = AdoptableAnimal.objects.filter(status='available').order_by('-created_at')
    return render(request, 'core/adoptions.html', {'animals': animals})

@login_required
def adopt_animal(request, animal_id):
    animal = get_object_or_404(AdoptableAnimal, id=animal_id, status='available')
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user
            adoption_request.animal = animal
            adoption_request.save()
            messages.success(request, 'Adoption request submitted successfully! We will contact you soon.')
            return redirect('adoptions')
    else:
        form = AdoptionRequestForm()
    return render(request, 'core/adopt_animal.html', {'animal': animal, 'form': form})

def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'core/products.html', {'products': products})

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock > 0:
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=1,
            total_price=product.price,
            status='completed'
        )
        product.stock -= 1
        product.save()
        return render(request, 'core/thank_you.html', {'order': order})
    else:
        messages.error(request, 'Product out of stock.')
        return redirect('products')

def services_view(request):
    plans = ServicePlan.objects.all().order_by('price')

    for p in plans:
        p.features_list = [item.strip() for item in p.features.split(',')]  # clean list

    return render(request, 'core/services.html', {'plans': plans})




@login_required
def book_service(request, plan_id):
    plan = get_object_or_404(ServicePlan, id=plan_id)

    # ADD THIS LINE ↓↓↓
    plan.features_list = plan.features.split(',')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service_plan = plan
            booking.payment_completed = True
            booking.status = 'confirmed'
            booking.save()
            messages.success(request, 'Booking confirmed! Thank you for choosing Pet Care.')
            return redirect('services')
    else:
        form = BookingForm()

    return render(request, 'core/book_service.html', {'plan': plan, 'form': form})


def about_view(request):
    return render(request, 'core/about.html')
