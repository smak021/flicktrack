from django.contrib import admin
from .models import ft_data, film_det,film_loc

# Register your models here.

@admin.register(ft_data)
class film(admin.ModelAdmin):
    list_display = ('film_name','theatre_id','show_id','Show_time','film_loc','show_date','total_seat','booked_seat','available_seat','last_modified')

@admin.register(film_det)
class film_det(admin.ModelAdmin):
    list_display = ('film_name','film_id','release_date','film_loc')

@admin.register(film_loc)
class film_loc(admin.ModelAdmin):
    list_display = ('film_location','venue_id')