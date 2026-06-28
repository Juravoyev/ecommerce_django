from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    next_url = request.GET.get('next', 'home')
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '')
        
        if not phone_number or not password:
            messages.error(request, "Telefon raqam va parolni kiriting.")
        else:
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(request, "Telefon raqam yoki parol xato.")
                
    return render(request, 'users/login.html', {'next': next_url})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    next_url = request.GET.get('next', 'home')
        
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        
        if not phone_number or not password:
            messages.error(request, "Telefon raqam va parolni kiriting.")
        elif User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        else:
            user = User.objects.create_user(
                phone_number=phone_number,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect(next_url)
            
    return render(request, 'users/signup.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('home')
