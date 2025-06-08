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

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    #  Step 2: Confirmation email has been sent
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    #  Step 3: Password reset link clicked, set new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    #  Step 4: Password reset complete
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
