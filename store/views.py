
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from decimal import Decimal
import json

from .models import Product, Order


def home(request):
    products = Product.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'index.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all fields.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
@require_POST
def place_order(request):
    try:
        data = json.loads(request.body)
        cart = data.get('cart', [])

        if not cart:
            return JsonResponse({
                'success': False,
                'message': 'Your cart is empty!'
            })

        total = Decimal('0.00')
        order_items = []

        for item in cart:
            product_id = int(item.get('id'))
            quantity = int(item.get('quantity', 1))

            if quantity < 1:
                raise ValueError('Invalid quantity')

            product = get_object_or_404(Product, pk=product_id)
            total += product.price * quantity
            order_items.append(f"{product.name} x {quantity}")

        Order.objects.create(
            user=request.user,
            products=', '.join(order_items),
            total_price=total
        )

        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully!'
        })

    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return JsonResponse({
            'success': False,
            'message': 'Invalid order details.'
        }, status=400)


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'orders.html', {'orders': orders})
