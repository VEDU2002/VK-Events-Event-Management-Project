from django.shortcuts import render, redirect, get_object_or_404
from eventapp.models import Event
from eventapp.forms import BookingForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import OTPRequestForm, OTPVerifyForm
from django.contrib.auth.hashers import make_password
import random
from .forms import OTPResetForm
from razorpay import Client

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def events(request):
    context = {
        'eve': Event.objects.all()
    }
    return render(request, "events.html", context)


def booking_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to book.")
        return redirect('login')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            # ✅ Send confirmation email
            send_mail(
                subject='Booking Confirmation',
                message=f"Hi {request.user.username},\n\nYour booking for has been confirmed.\n\nThank you!.We will contact will you about event sooner",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            messages.success(request, "Booking confirmed and confirmation email sent.")
            return redirect('index')
    else:
        form = BookingForm()

    # ✅ Razorpay client and order creation
    client = Client(auth=('rzp_test_J3K0nbI279n8zQ', 'NL45n1iC9tkA6Dl0AS9svNPL'))
    payment = client.order.create({'amount': 10000, 'currency': 'INR', 'payment_capture': 1})

    return render(request, 'booking.html', {
        'form': form,
        'razorpay_key': 'rzp_test_J3K0nbI279n8zQ',
        'payment': payment
    })

def contact(request):
    return render(request, "contact.html")

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    sub_cards = event.subcards.all()
    return render(request, 'event_detail.html', {
        'event': event,
        'sub_cards': sub_cards
    })


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            # Create the user
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, f"Registered successfully as {username}!")
                return redirect('login')  # Redirect to your login URL name

    return render(request, 'register.html')


# Your existing views (index, about, events, booking_view, contact, event_detail, register)...

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')  # Can be username or email
        password = request.POST.get('password')
        
        print(f"=== LOGIN DEBUG ===")
        print(f"Identifier: '{identifier}'")
        print(f"Password length: {len(password) if password else 0}")
        print(f"POST data: {dict(request.POST)}")

        if not identifier or not password:
            messages.error(request, 'Please enter both username/email and password.')
            return render(request, 'log.html')

        identifier = identifier.strip()
        
        # Resolve username from email if needed
        user = None
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=identifier, password=password)

        print(f"Authentication result: {user}")

        if user is not None:
            if user.is_active:
                login(request, user)
                print(f"User '{user.username}' logged in successfully")
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('index')
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'log.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

# OTP Storage - In production, use database or cache
otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def reset_via_otp(request):
    if request.method == 'POST':
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                otp_storage[email] = otp
                
                print(f"=== OTP GENERATION ===")
                print(f"Email: {email}")
                print(f"Generated OTP: {otp}")
                print(f"OTP Storage: {dict(otp_storage)}")
                
                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is: {otp}\n\nThis OTP is valid for password reset.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email.')
                # Pass email as URL parameter
                return redirect(f'/verify-otp/?email={email}')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email.')
            except Exception as e:
                print(f"Error sending OTP: {e}")
                messages.error(request, 'Error sending OTP. Please try again.')
    else:
        form = OTPRequestForm()
    return render(request, 'reset_via_otp.html', {'form': form})

def verify_otp(request):
    if request.method == "POST":
        form = OTPResetForm(request.POST)
        
        print(f"=== OTP VERIFICATION DEBUG ===")
        print(f"POST data: {dict(request.POST)}")
        print(f"Form is valid: {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        print(f"Current OTP storage: {dict(otp_storage)}")
        
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            
            print(f"Email: '{email}'")
            print(f"Entered OTP: '{otp}'")
            print(f"Stored OTP: '{otp_storage.get(email)}'")
            print(f"New password length: {len(new_password)}")

            try:
                user = User.objects.get(email=email)
                print(f"User found: {user.username}")
                
                # Check OTP
                stored_otp = otp_storage.get(email)
                if stored_otp and stored_otp == otp:
                    # Update password
                    user.set_password(new_password)
                    user.save()
                    
                    # Clear used OTP
                    otp_storage.pop(email, None)
                    print("Password updated successfully")
                    
                    # Test the new password immediately
                    test_user = authenticate(username=user.username, password=new_password)
                    print(f"Password test result: {test_user}")
                    
                    messages.success(request, "Password reset successful. Please login with your new password.")
                    return redirect("login")
                else:
                    print(f"OTP mismatch - Entered: '{otp}', Stored: '{stored_otp}'")
                    messages.error(request, "Invalid OTP. Please try again.")
            except User.DoesNotExist:
                print(f"User not found with email: {email}")
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        # GET request - show form with email pre-filled
        email = request.GET.get('email', '')
        form = OTPResetForm(initial={'email': email})
        print(f"GET request - Email from URL: '{email}'")

    return render(request, "verify_otp.html", {"form": form})
