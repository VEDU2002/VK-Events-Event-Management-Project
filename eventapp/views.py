from django.shortcuts import render, redirect, get_object_or_404
from eventapp.models import Event
from eventapp.forms import BookingForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

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
        messages.error(request, "Please register or login before booking.")
        return redirect('register')  # or 'login' if you prefer login first

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            # Send confirmation email to the user
            send_mail(
                subject='Booking Confirmation',
                message=f'Dear {request.user.first_name},\n\nYour booking for "{booking.event.name}" on {booking.booking_date} has been successfully received.\n\nThank you!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            # Notify backend (admin) via email
            send_mail(
                subject='New Booking Received',
                message=f'New booking by {booking.cus_name} ({request.user.email}) for event "{booking.event.name}" on {booking.booking_date}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return redirect('index')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Replace 'home' with your homepage view name
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'log.html')

def logout_view(request):
    logout(request)
    return redirect('index') 