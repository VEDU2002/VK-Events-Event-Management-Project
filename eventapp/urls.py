from django.urls import path
from eventapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('booking/', views.booking_view, name='booking'),  # updated here
    path('contact/', views.contact, name='contact'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
    path('register/', views.register, name='register'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-otp/', views.reset_via_otp, name='reset_via_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
