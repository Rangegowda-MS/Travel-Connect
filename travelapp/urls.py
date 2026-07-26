from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserLoginForm

urlpatterns = [

    # ================= HOME =================
    path('', views.IndexView, name='home'),

    # ================= AUTH =================
    path(
        'accounts/login/',
        LoginView.as_view(authentication_form=UserLoginForm),
        name='login_url'
    ),

    path(
        'register/',
        views.registerView,
        name='register_url'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    # ================= SEARCH =================
    path(
        'package/',
        views.PackageView,
        name='package'
    ),

    path(
        'flights/',
        views.FlightView,
        name='flights'
    ),

    path(
        'hotels/',
        views.HotelView,
        name='hotels'
    ),

    path(
        'places/',
        views.PlacesView,
        name='places'
    ),

    # ================= FLIGHT BOOKING =================
    path(
        'bookflight/<str:flight_num>/<str:date>/',
        views.Flightbook,
        name='bookflight'
    ),

    path(
        'userflight/<str:flight_num>/<str:date>/<int:seat>/',
        views.FlightSubmit,
        name='userflight'
    ),

    # ================= HOTEL BOOKING =================
    path(
        'bookhotel/<str:hotel>/<str:date>/',
        views.Hotelbook,
        name='bookhotel'
    ),

    path(
        'userhotel/<str:hotel>/<str:date>/<int:room>/',
        views.HotelSubmit,
        name='userhotel'
    ),

    # ================= PACKAGE BOOKING =================
    path(
        'bookpackage/<str:source>/<str:city>/<str:date>/',
        views.PackageBook,
        name='bookpackage'
    ),

    path(
        'userpackage/<str:flight>/<str:hotel>/<str:date>/<int:room>/<int:seat>/',
        views.PackageSubmit,
        name='userpackage'
    ),

    # ================= CANCEL FLIGHT =================
    path(
        'cancelflight/<str:flight>/<str:date>/<int:seat>/',
        views.CancelFlight,
        name='cancelflight'
    ),

    path(
        'confirm-cancelflight/<str:flight>/<str:date>/<int:seat>/',
        views.ConfirmCancelFlight,
        name='confirm_cancelflight'
    ),

    path(
        'concanflight/<str:flight>/<str:date>/<int:seat>/',
        views.ConfirmCancelFlight,
        name='concanflight'
    ),

    # ================= CANCEL HOTEL =================
    path(
        'cancelhotel/<str:hotel>/<str:date>/<int:room>/',
        views.CancelHotel,
        name='cancelhotel'
    ),

    path(
        'confirm-cancelhotel/<str:hotel>/<str:date>/<int:room>/',
        views.ConfirmCancelHotel,
        name='confirm_cancelhotel'
    ),

    path(
        'concanhotel/<str:hotel>/<str:date>/<int:room>/',
        views.ConfirmCancelHotel,
        name='concanhotel'
    ),

    # ================= CANCEL PACKAGE =================
    path(
        'cancelpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>/',
        views.CancelPackage,
        name='cancelpackage'
    ),

    path(
        'confirm-cancelpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>/',
        views.ConfirmCancelPackage,
        name='confirm_cancelpackage'
    ),

    path(
        'concanpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>/',
        views.ConfirmCancelPackage,
        name='concanpackage'
    ),

    # ================= PAYMENT =================
    path(
        'payment/',
        views.payment_page,
        name='payment'
    ),

    path(
        'payment-success/',
        views.payment_success,
        name='payment_success'
    ),

    path(
        'payment/<str:flight_num>/<str:hotel_name>/<str:date>/<int:roomreq>/<int:seatsreq>/',
        views.payment,
        name='payment_with_booking'
    ),

    # ================= DASHBOARD =================
    path(
        'dashboard/',
        views.Dashboard,
        name='dashboard'
    ),

    # ================= OTHER =================
    path(
        'forgot-password/',
        views.forgot_password_view,
        name='forgot_password'
    ),

    path(
        'clear-all-bookings/',
        views.clear_all_bookings,
        name='clear_all_bookings'
    ),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)