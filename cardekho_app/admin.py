from django.contrib import admin
from .models import car_list, Showroomlist, Review

# Register your models here.
admin.site.register(car_list)
admin.site.register(Showroomlist)
admin.site.register(Review)

