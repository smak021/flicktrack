
from django.db import models
# Create your models here.
#New Simple Table

STATUS_CHOICE = [
    ('active','Active'),
    ('inactive','Inactive'),
    ('stopped','Stopped')
]


class film(models.Model):
    film_id = models.CharField(max_length=50, primary_key=True)
    film_name = models.CharField(max_length=100)
    cover_url = models.CharField(max_length=500)        
    release_date = models.CharField(max_length=50)
    film_story = models.CharField(max_length=2000)
    film_genre = models.CharField(max_length=50)
    film_censor = models.CharField(max_length=50)
    film_duration = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    film_status = models.CharField(max_length=30,default="active",choices=STATUS_CHOICE)
    cast_n_crew = models.CharField(max_length=1000)
    tn_code = models.CharField(max_length=50,default="NA")
    ptm_code = models.CharField(max_length=50, default="NA")
   

    def __str__(self):
        return self.film_id

class status(models.Model):
    film = models.OneToOneField(film,on_delete=models.CASCADE,primary_key=True)
    is_tracking = models.BooleanField(default=True)

    def __str__(self):
        return self.film_id

class mdata(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True)
    show_date = models.CharField(max_length=50)
    show_count = models.IntegerField(default=0)
    category_name = models.CharField(max_length=50,blank=True)
    price = models.CharField(max_length=50,blank=True)
    booked_seats = models.CharField(max_length=50,default="0")
    available_seats = models.CharField(max_length=50, default="0")
    total_seats = models.CharField(max_length=50,default="0")
    film = models.ForeignKey(film,on_delete=models.CASCADE)
    theatre_code = models.CharField(max_length=50)
    theatre_location = models.CharField(max_length=50)
    theatre_name = models.CharField(max_length=500,default="Not Available")
    last_modified = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

class track(models.Model):
    track_id = models.AutoField(auto_created=True, primary_key=True)
    track_location = models.CharField(max_length=50)
    is_currently_tracking = models.CharField(max_length=50, default="Y")
    loc_real_name = models.CharField(max_length=50)
    theatre_code = models.CharField(max_length=30,default="null")
    source = models.CharField(max_length=30,default="bms")
    offset = models.CharField(max_length=40,default='na')
    offset_check = models.CharField(max_length=2000,default='na')

    def __str__(self):
        return self.track_id

class show(models.Model):
    show_id = models.CharField(max_length=50,primary_key=True)
    show_time = models.CharField(max_length=50)
    screen_name = models.CharField(max_length=50,blank=True)
    show_date = models.CharField(max_length=50)
    theatre_code = models.CharField(max_length=50)
    film = models.ForeignKey(film,on_delete=models.CASCADE)
    last_modified = models.CharField(max_length=50,default='na')

