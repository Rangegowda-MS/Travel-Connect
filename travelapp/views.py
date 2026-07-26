from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
import random

from .forms import (
    SignUpForm,
    HotelForm,
    FlightForm,
    ChoiceForm,
    SeatForm,
    RoomForm,
    CityForm
)

from .models import (
    Flights,
    Hotels,
    Famous,
    BookFlight,
    BookHotel,
    BookPackage,
    City
)



# =========================
# HOME
# =========================

def IndexView(request):
    return render(request, 'index.html')


# =========================
# REGISTER
# =========================

def registerView(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect('login_url')

    else:
        form = SignUpForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


# =========================
# PACKAGE SEARCH
# =========================

def PackageView(request):

    form = FlightForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            source = form.cleaned_data['source'].upper()
            destination = form.cleaned_data['destination'].upper()

            # IMPORTANT FIX
            date = str(form.cleaned_data['date'])

            flights = Flights.objects.filter(
                source__iexact=source,
                destination__iexact=destination
            )

            hotels = Hotels.objects.filter(
                city__city__iexact=destination
            )

            famplace = Famous.objects.filter(
                city__city__iexact=destination
            )

            if hotels.exists():
                city = destination
            else:
                city = destination

                messages.warning(
                    request,
                    "No hotels found for this destination."
                )

            response = {
                'Flights': flights,
                'Hotels': hotels,
                'Famplace': famplace,
                'form': form,
                'date': date,
                'source': source,
                'city': city,
            }

            return render(
                request,
                'package.html',
                response
            )

        else:

            messages.error(
                request,
                "Invalid form data."
            )

    return render(
        request,
        'package.html',
        {'form': form}
    )


# =========================
# HOTEL SEARCH
# =========================

def HotelView(request):

    form = HotelForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            city = form.cleaned_data['city'].upper()

            # IMPORTANT FIX
            date = str(form.cleaned_data['date'])

            hotels = Hotels.objects.filter(
                city__city__iexact=city
            )

            if not hotels.exists():
                messages.warning(
                    request,
                    "No hotels found."
                )

            response = {
                'Hotels': hotels,
                'date': date,
                'form': form
            }

            return render(
                request,
                'hotels.html',
                response
            )

    return render(
        request,
        'hotels.html',
        {'form': form}
    )


# =========================
# FLIGHT SEARCH
# =========================

def FlightView(request):

    form = FlightForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            source = form.cleaned_data['source'].upper()
            destination = form.cleaned_data['destination'].upper()

            # IMPORTANT FIX
            date = str(form.cleaned_data['date'])

            flights = Flights.objects.filter(
                source__iexact=source,
                destination__iexact=destination
            )

            if not flights.exists():
                messages.warning(
                    request,
                    "No flights found."
                )

            response = {
                'Flights': flights,
                'date': date,
                'form': form
            }

            return render(
                request,
                'flights.html',
                response
            )

    return render(
        request,
        'flights.html',
        {'form': form}
    )


# =========================
# DASHBOARD
# =========================

@login_required
def Dashboard(request):

    user = request.user

    flights = BookFlight.objects.filter(
        username_id=user
    )

    hotels = BookHotel.objects.filter(
        username_id=user
    )

    packages = BookPackage.objects.filter(
        username_id=user
    )

    response = {
        'flights': flights,
        'hotels': hotels,
        'packages': packages
    }

    return render(
        request,
        'dashboard.html',
        response
    )


# =========================
# BOOK FLIGHT
# =========================

@login_required
def Flightbook(request, flight_num=None, date=None):

    form = SeatForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            seats = form.cleaned_data['seats']

            flight = Flights.objects.filter(
                flight_num=flight_num
            ).first()

            if not flight:

                messages.error(
                    request,
                    "Flight not found."
                )

                return redirect('flights')

            booked1 = BookFlight.objects.filter(
                flight=flight.flight_num,
                date=date
            )

            booked2 = BookPackage.objects.filter(
                flight=flight.flight_num,
                date=date
            )

            booked_seats = 0

            for i in booked1:
                booked_seats += i.seat

            for i in booked2:
                booked_seats += i.seat

            seatrem = flight.seats - booked_seats

            availability = "available"

            if seats > seatrem:
                availability = "unavailable"

            price = seats * flight.eprice

            response = {
                'flight': [flight],
                'date': date,
                'form': form,
                'seatrem': seatrem,
                'availability': availability,
                'seatsreq': seats,
                'price': price
            }

            return render(
                request,
                'bookflight.html',
                response
            )

    return render(
        request,
        'bookflight.html',
        {'form': form}
    )


@login_required
def FlightSubmit(request, flight_num=None, date=None, seat=None):

    user = request.user

    booking = BookFlight(
        username_id=user,
        flight=flight_num,
        date=date,
        seat=seat
    )

    booking.save()

    messages.success(
        request,
        "Flight booked successfully."
    )

    return redirect('dashboard')


# =========================
# BOOK HOTEL
# =========================

@login_required
def Hotelbook(request, hotel=None, date=None):

    form = RoomForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            rooms = form.cleaned_data['rooms']

            hotel_obj = Hotels.objects.filter(
                hotel_name=hotel
            ).first()

            if not hotel_obj:

                messages.error(
                    request,
                    "Hotel not found."
                )

                return redirect('hotels')

            booked1 = BookHotel.objects.filter(
                hotel_name=hotel_obj.hotel_name,
                date=date
            )

            booked2 = BookPackage.objects.filter(
                hotel_name=hotel_obj.hotel_name,
                date=date
            )

            booked_rooms = 0

            for i in booked1:
                booked_rooms += i.room

            for i in booked2:
                booked_rooms += i.room

            roomrem = hotel_obj.rooms - booked_rooms

            availability = "available"

            if rooms > roomrem:
                availability = "unavailable"

            price = rooms * hotel_obj.hotel_price

            response = {
                'hotel': [hotel_obj],
                'date': date,
                'form': form,
                'roomrem': roomrem,
                'availability': availability,
                'roomreq': rooms,
                'price': price
            }

            return render(
                request,
                'bookhotel.html',
                response
            )

    return render(
        request,
        'bookhotel.html',
        {'form': form}
    )


@login_required
def HotelSubmit(request, hotel=None, date=None, room=None):

    user = request.user

    booking = BookHotel(
        username_id=user,
        hotel_name=hotel,
        date=date,
        room=room
    )

    booking.save()

    messages.success(
        request,
        "Hotel booked successfully."
    )

    return redirect('dashboard')


# =========================
# PACKAGE BOOKING
# =========================
@login_required
def PackageBook(request, source, city, date):

    form = ChoiceForm(request.POST or None)

    allflights = Flights.objects.filter(
        source__iexact=source,
        destination__iexact=city
    )

    allhotels = Hotels.objects.filter(
        city__city__iexact=city
    )

    # FIRST PAGE LOAD
    response = {
        'Flights': allflights,
        'Hotels': allhotels,
        'allflights': allflights,
        'allhotels': allhotels,
        'form': form,
        'date': date,
        'source': source,
        'city': city
    }

    if request.method == "POST":

        if form.is_valid():

            flight_no = (form.cleaned_data.get('flight') or '').upper()
            hotel_name = form.cleaned_data.get('hotel')

            seats = form.cleaned_data.get('seats')
            rooms = form.cleaned_data.get('rooms')

            flight = Flights.objects.filter(
                flight_num=flight_no
            ).first()

            hotel = Hotels.objects.filter(
                hotel_name=hotel_name
            ).first()

            if not flight or not hotel:

                messages.error(
                    request,
                    "Please select a valid flight and hotel."
                )

                return render(
                    request,
                    'bookpackage.html',
                    response
                )

            # ========================
            # FLIGHT AVAILABILITY
            # ========================

            booked_flights1 = BookFlight.objects.filter(
                flight=flight.flight_num,
                date=date
            )

            booked_flights2 = BookPackage.objects.filter(
                flight=flight.flight_num,
                date=date
            )

            booked_seats = 0

            for i in booked_flights1:
                booked_seats += i.seat

            for i in booked_flights2:
                booked_seats += i.seat

            seatrem = flight.seats - booked_seats

            flavailability = "available"

            if seats > seatrem:
                flavailability = "unavailable"

            # ========================
            # HOTEL AVAILABILITY
            # ========================

            booked_hotels1 = BookHotel.objects.filter(
                hotel_name=hotel.hotel_name,
                date=date
            )

            booked_hotels2 = BookPackage.objects.filter(
                hotel_name=hotel.hotel_name,
                date=date
            )

            booked_rooms = 0

            for i in booked_hotels1:
                booked_rooms += i.room

            for i in booked_hotels2:
                booked_rooms += i.room

            roomrem = hotel.rooms - booked_rooms

            havailability = "available"

            if rooms > roomrem:
                havailability = "unavailable"

            response = {
                'Flights': [flight],
                'Hotels': [hotel],

                'allflights': allflights,
                'allhotels': allhotels,

                'form': form,
                'date': date,

                'flavailability': flavailability,
                'seatrem': seatrem,
                'seatsreq': seats,
                'pricef': seats * flight.eprice,

                'havailability': havailability,
                'roomrem': roomrem,
                'roomreq': rooms,
                'priceh': rooms * hotel.hotel_price
            }

            return render(
                request,
                'bookpackage.html',
                response
            )

    return render(
        request,
        'bookpackage.html',
        response
    )


@login_required
def PackageSubmit(
    request,
    flight=None,
    hotel=None,
    date=None,
    room=None,
    seat=None
):

    user = request.user

    booking = BookPackage(
        username_id=user,
        flight=flight,
        seat=seat,
        hotel_name=hotel,
        room=room,
        date=date
    )

    booking.save()

    messages.success(
        request,
        "Package booked successfully."
    )

    return redirect('dashboard')


# =========================
# CANCEL FLIGHT
# =========================

@login_required
def CancelFlight(request, flight=None, date=None, seat=None):

    flight_obj = Flights.objects.filter(
        flight_num=flight
    ).first()

    if not flight_obj:
        return redirect('dashboard')

    price = seat * flight_obj.eprice

    response = {
        'Flight': [flight_obj],
        'price': price,
        'seat': seat,
        'date': date
    }

    return render(
        request,
        'cancelflight.html',
        response
    )


@login_required
def ConfirmCancelFlight(request, flight=None, date=None, seat=None):

    user = request.user

    booking = BookFlight.objects.filter(
        username_id=user,
        flight=flight,
        date=date,
        seat=seat
    )

    booking.delete()

    messages.success(
        request,
        "Flight booking cancelled."
    )

    return redirect('dashboard')


# =========================
# CANCEL HOTEL
# =========================

@login_required
def CancelHotel(request, hotel=None, date=None, room=None):

    hotel_obj = Hotels.objects.filter(
        hotel_name=hotel
    ).first()

    if not hotel_obj:
        return redirect('dashboard')

    price = room * hotel_obj.hotel_price

    response = {
        'Hotel': [hotel_obj],
        'price': price,
        'room': room,
        'date': date
    }

    return render(
        request,
        'cancelhotel.html',
        response
    )


@login_required
def ConfirmCancelHotel(request, hotel=None, date=None, room=None):

    user = request.user

    booking = BookHotel.objects.filter(
        username_id=user,
        hotel_name=hotel,
        date=date,
        room=room
    )

    booking.delete()

    messages.success(
        request,
        "Hotel booking cancelled."
    )

    return redirect('dashboard')


# =========================
# CANCEL PACKAGE
# =========================

@login_required
def CancelPackage(
    request,
    flight=None,
    seat=None,
    hotel=None,
    date=None,
    room=None
):

    flight_obj = Flights.objects.filter(
        flight_num=flight
    ).first()

    hotel_obj = Hotels.objects.filter(
        hotel_name=hotel
    ).first()

    if not flight_obj or not hotel_obj:
        return redirect('dashboard')

    response = {
        'Flight': [flight_obj],
        'Hotel': [hotel_obj],
        'pricef': seat * flight_obj.eprice,
        'priceh': room * hotel_obj.hotel_price,
        'seat': seat,
        'room': room,
        'date': date
    }

    return render(
        request,
        'cancelpackage.html',
        response
    )


@login_required
def ConfirmCancelPackage(
    request,
    flight=None,
    seat=None,
    hotel=None,
    date=None,
    room=None
):

    user = request.user

    package = BookPackage.objects.filter(
        username_id=user,
        hotel_name=hotel,
        date=date,
        room=room,
        flight=flight,
        seat=seat
    )

    package.delete()

    messages.success(
        request,
        "Package cancelled successfully."
    )

    return redirect('dashboard')


# =========================
# PAYMENT
# =========================

def payment(
    request,
    flight_num,
    hotel_name,
    date,
    roomreq,
    seatsreq
):

    flight = Flights.objects.filter(
        flight_num=flight_num
    ).first()

    hotel = Hotels.objects.filter(
        hotel_name=hotel_name
    ).first()

    flight_price = 0
    hotel_price = 0

    if flight:
        flight_price = int(seatsreq) * flight.eprice

    if hotel:
        hotel_price = int(roomreq) * hotel.hotel_price

    total_amount = flight_price + hotel_price

    context = {
        'flight_num': flight_num,
        'hotel_name': hotel_name,
        'date': date,
        'roomreq': roomreq,
        'seatsreq': seatsreq,
        'amount': total_amount,
    }

    return render(
        request,
        'payment.html',
        context
    )

def payment_page(request):

    booking_type = request.GET.get(
        'type',
        'unknown'
    )

    return render(
        request,
        'payment.html',
        {'booking_type': booking_type}
    )


def payment_success(request):

    transaction_id = "TC" + str(
        random.randint(
            100000000,
            999999999
        )
    )

    context = {

        "transaction_id": transaction_id,

        "payment_date":
        datetime.now().strftime(
            "%d-%m-%Y"
        ),

        "payment_time":
        datetime.now().strftime(
            "%I:%M:%S %p"
        ),

        "amount":
        request.POST.get(
            "amount",
            "0"
        ),

        "status":
        "SUCCESS",

        "payment_method":
        "Credit/Debit Card",

        "booking_reference":
        "BK" + str(
            random.randint(
                100000,
                999999
            )
        )
    }

    return render(
        request,
        "payment_success.html",
        context
    )


# =========================
# PLACES
# =========================

def PlacesView(request):

    form = CityForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            city = form.cleaned_data['city'].upper()

            famplace = Famous.objects.filter(
                city__city__iexact=city
            )

            if not famplace.exists():

                messages.warning(
                    request,
                    "No famous places found."
                )

            response = {
                'form': form,
                'Famplace': famplace
            }

            return render(
                request,
                'places.html',
                response
            )

    return render(
        request,
        'places.html',
        {'form': form}
    )


# =========================
# FORGOT PASSWORD
# =========================

def forgot_password_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        new_password = request.POST.get('new_password')

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if new_password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect('forgot_password')

        try:

            user = User.objects.get(
                username=username
            )

            user.set_password(new_password)

            user.save()

            messages.success(
                request,
                "Password reset successfully."
            )

            return redirect('login_url')

        except User.DoesNotExist:

            messages.error(
                request,
                "User not found."
            )

            return redirect('forgot_password')

    return render(
        request,
        'forgot_password.html'
    )
# =========================
# CLEAR ALL BOOKINGS
# =========================

@login_required
def clear_all_bookings(request):

    user = request.user

    # delete all user bookings
    BookFlight.objects.filter(username_id=user).delete()
    BookHotel.objects.filter(username_id=user).delete()
    BookPackage.objects.filter(username_id=user).delete()

    messages.success(
        request,
        "All your bookings have been cleared successfully."
    )

    return redirect('dashboard')