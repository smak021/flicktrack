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
    booked_seat = models.IntegerField()
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
    film_id = models.CharField(max_length=100)
    release_date=models.CharField(max_length=50)
    film_loc = models.CharField(max_length=100)
    
    def __str__(self):
        return self.film_name

class film_loc(models.Model):
    film_location = models.CharField(max_length=100)
    venue_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.film_location



