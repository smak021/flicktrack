from pyexpat import model
from unicodedata import category
from django.db import models
import sched
# Create your models here.

class ft_data(models.Model):
    film_name = models.CharField(max_length=100)
    film_id = models.CharField(max_length=100)
    theatre_id = models.CharField(max_length=100)
    show_id = models.CharField(max_length=100)
    available_seat = models.IntegerField()
    total_seat = models.IntegerField()
    category_name=models.CharField(max_length=50,default='Normal')
    booked_seat = models.IntegerField()
    screen_name=models.CharField(max_length=50,default='Not set')
    Show_time = models.CharField(max_length=100)
    show_date = models.CharField(max_length=100)
    price=models.CharField(max_length=30)
    film_loc = models.CharField(max_length=50,default="not set")
    last_modified = models.CharField(max_length=100)


    class Meta:
        ordering = ("show_date","theatre_id")


    def __str__(self):
        return self.film_name

class film_det(models.Model):
    film_name = models.CharField(max_length=100)
    film_real_name=models.CharField(max_length=100,default='Not Set')
    film_id = models.CharField(max_length=100)
    release_date=models.CharField(max_length=50)
    image_url = models.CharField(max_length=150,default='18am-padi-et00105977-28-06-2019-01-18-50')
    film_loc = models.CharField(max_length=100)
    film_length=models.CharField(max_length=50, default="Not Available")
    film_genre=models.CharField(max_length=50, default="Not Available")
    film_story=models.CharField(max_length=500, default="Not Available")
    film_censor=models.CharField(max_length=50, default="Not Available")
    def __str__(self):
        return self.film_name

class film_loc(models.Model):
    film_location = models.CharField(max_length=100)
    venue_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.film_location



