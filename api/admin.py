from django.contrib import admin
#from .models import ft_data, film_det,film_loc
# from .models import film, show, track

# Register your models here.

# @admin.register(film)
# class films(admin.ModelAdmin):
#     list_display = ('film_id', 'film_name', 'cover_url', 'release_date', 'film_story', 'film_genre', 'film_censor', 'film_duration')


# @admin.register(show)
# class shows(admin.ModelAdmin):
#     list_display = ('show_id', 'film_id', 'show_time', 'screen_name', 'show_date')


# @admin.register(track)
# class track(admin.ModelAdmin):
#     list_display = ('track_id', 'track_location', 'is_currently_tracking')


#@admin.register(ft_data)
#class film(admin.ModelAdmin):
 #   list_display = ('film_name','category_name','theatre_id','show_id','Show_time','film_loc','show_date','total_seat','booked_seat','price','available_seat','last_modified')

#@admin.register(film_det)
#class film_det(admin.ModelAdmin):
 #   list_display = ('film_name','film_real_name','film_id','release_date','image_url','film_loc')

#@admin.register(film_loc)
#class film_loc(admin.ModelAdmin):
#    list_display = ('film_location','venue_id')