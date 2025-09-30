
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db.models import Q

from bookings.models import Room, Staff, Booking
from bookings.forms import BookingForm


class BookingList(View):

    def get(self, request):
        query = request.GET

        bookings = Booking.objects.filter(start_time__gt=timezone.localtime()).order_by("start_time")

        if query.get("search"):
            bookings = bookings.filter(
                Q(room__name__icontains=query.get("search")) | 
                Q(staff__name__icontains=query.get("search"))
            )

        return render(request, "booking-list.html", {
            "bookings": bookings
        })


class BookingCreate(View):

    def get(self, request):
        rooms = Room.objects.all()
        staffs = Staff.objects.all()
        
        return render(request, "booking.html", {
            "rooms": rooms,
            "staffs": staffs
        })

    def post(self, request):
        error = ""
        data = request.POST
        start_time_str = f'{data["start_date"]} {data["start_time"]}'
        end_time_str = f'{data["end_date"]} {data["end_time"]}'
        start_time = timezone.make_aware(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M"))
        end_time = timezone.make_aware(datetime.strptime(end_time_str, "%Y-%m-%d %H:%M"))
        
        duration = end_time - start_time
        bookings = Booking.objects.filter(start_time__lte=end_time, end_time__gte=start_time, room_id=data["room"])
        
        if end_time < start_time:
            error = "End time cannot be before start time"
        
        elif bookings.count() > 0:
            error = "This room has already been booked for the selected time"

        if not error:
            Booking.objects.create(
                staff_id=data["staff"],
                room_id=data["room"],
                start_time=start_time,
                end_time=end_time,
                purpose=data["purpose"]
            )
            return redirect('booking-list')
        else:
            rooms = Room.objects.all()
            staffs = Staff.objects.all()
            return render(request, "booking.html", {
            "rooms": rooms,
            "staffs": staffs,
            "error": error
        })

class BookingDelete(View):

    def get(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        booking.delete()

        return redirect("booking-list")
    
class BookingCreate(View):

    def get(self, request):
        form = BookingForm()
        return render(request, "booking.html", {
            "form": form,
        })

    def post(self, request):
        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('booking-list')

        return render(request, "booking.html", {
            "form": form
        })