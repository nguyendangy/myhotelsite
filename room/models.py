from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

from accounts.models import Guest
# Create your models here.

def upload_room_images(instance,filename):
    return "Room/Images/{room}/{filename}/".format(room=instance.room,filename=filename)


def upload_cover_image(instance,filename):
    return "Room/cover/{id}/{filename}/".format(id=instance.id,filename=filename)

class Room(models.Model):
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),

    )

    ROOM_ADDRESS = (
        ('Ha Noi','Ha Noi'),
        ('Da Nang','Da Nang'),
        ('Ho Chi Minh','Ho Chi Minh'),
    )

    ROOM_INCLUDE = (
        ('Nha tam','Nha tam'),
        ('Nha bep','Nha bep'),
        ('Ban an','Ban an'),
    )
    
    number = models.IntegerField(primary_key=True)
    capacity = models.SmallIntegerField()
    numberOfBeds = models.SmallIntegerField()
    # roomType = models.CharField(max_length=20, choices=ROOM_TYPES)
    roomType = models.TextField(max_length=20)

    price = models.FloatField()
    statusStartDate = models.DateField(null=True)
    statusEndDate = models.DateField(null=True)
    address = models.CharField(max_length=20, choices=ROOM_ADDRESS)
    hotel_name = models.CharField(max_length=20, default='hotelname')
    rate = models.FloatField(default=0.0)
    # room_include = MultiSelectField(choices=ROOM_INCLUDE,max_choices=3, max_length=20)
    room_include = models.TextField( max_length=30, default='room_include')

    # images = models.ImageField(upload_to="images", default="none")
    price_discount = models.FloatField(default=0.0)
    price_discount_percent = models.FloatField(default=0.0)

    # cover_image = models.ImageField(upload_to =upload_room_images, blank=False )
    images= models.ImageField(blank=False,upload_to='images/photo/')
    
    # def __str__(self):
    #     return "Room-{id}".format(id=str(self.id))

    # def image_url(self):
    #         if self.images and hasattr(self.images, 'url'):
    #             return self.images.url

    def __str__(self):
        return str(self.number) 


# class Room_image(models.Model):
#     # room=room=models.ForeignKey(Room,on_delete=models.SET_NULL,null=True,blank=True)
#     # image=models.ImageField(null=True ,blank=True)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE ,related_name='room_images')
#     room_image = models.ImageField(upload_to=upload_room_images,null=False, blank=False)
  
    # def __str__(self):
    #     return str(self.room)

class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def numOfDep(self):
        return Dependees.objects.filter(booking=self).count()

    def numOfBooking(self):
        return Booking.objects.filter(guest=self).count()
        # return self.bookings_set.filter(guest=self).count()

    def numOfDays(self):
        totalDay = 0
        bookings = Booking.objects.filter(guest=self)
        # bookings = self.bookings_set.filter(guest=self)
        for b in bookings:
            day = b.endDate - b.startDate
            totalDay += int(day.days)

        return totalDay

    def numOfLastBookingDays(self):
        try:
            return int((Booking.objects.filter(guest=self).last().endDate - Booking.objects.filter(guest=self).last().startDate).days)
            # return int((self.bookings_set.filter(guest=self).last().endDate - self.bookings.filter(guest=self).last().startDate).days)
        except:
            return 0

    def currentRoom(self):
        booking = Booking.objects.filter(guest=self).last()
        # booking = self.bookings.filter(guest=self).last()

        return booking.roomNumber

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)


class Dependees(models.Model):
    booking = models.ForeignKey(Booking,   null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def str(self):
        return str(self.booking) + " " + str(self.name)


class Refund(models.Model):
    guest = models.ForeignKey(Guest,   null=True, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return str(self.guest)


class RoomServices(models.Model):
    SERVICES_TYPES = (
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning'),
        ('Technical', 'Technical'),
    )

    curBooking = models.ForeignKey(
        Booking,   null=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    createdDate = models.DateField(default=timezone.now)
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES)
    price = models.FloatField()

    def str(self):
        return str(self.curBooking) + " " + str(self.room) + " " + str(self.servicesType)
