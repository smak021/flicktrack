from cgi import print_exception
from pickle import TRUE
from pyexpat import model
from unicodedata import category
from django.db import models
# Create your models here.
#New Simple Table


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
    cast_n_crew = models.CharField(max_length=1000)

    def __str__(self):
        return self.film_id

class status(models.Model):
    film = models.OneToOneField(film,on_delete=models.CASCADE,primary_key=TRUE)
    is_tracking = models.BooleanField(default=True)

    def __str__(self):
        return self.film_id

class show(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True)
    show_id = models.CharField(max_length=50)
    show_time = models.CharField(max_length=50)
    screen_name = models.CharField(max_length=50)
    show_date = models.CharField(max_length=50)
    category_name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    booked_seats = models.CharField(max_length=50,default="0")
    available_seats = models.CharField(max_length=50, default="0")
    total_seats = models.CharField(max_length=50,default="0")
    film = models.ForeignKey(film,on_delete=models.CASCADE)
    theatre_code = models.CharField(max_length=50)
    theatre_location = models.CharField(max_length=50)
    last_modified = models.CharField(max_length=50)

    def __str__(self):
        return "%s %s" %(self.show_id,self.category_name)

class track(models.Model):
    track_id = models.AutoField(auto_created=True, primary_key=True)
    track_location = models.CharField(max_length=50)
    is_currently_tracking = models.CharField(max_length=50, default="Y")
    loc_real_name = models.CharField(max_length=50)

    def __str__(self):
        return self.track_id


#REBUILD

# # put & get done
# class film(models.Model):
#     film_id = models.CharField(max_length=50, primary_key=True)
#     film_name = models.CharField(max_length=100)
#     cover_url = models.CharField(max_length=500)        
#     release_date = models.CharField(max_length=50)
#     film_story = models.CharField(max_length=1500)
#     film_genre = models.CharField(max_length=50)
#     film_censor = models.CharField(max_length=50)
#     film_duration = models.CharField(max_length=50)

#     def __str__(self):
#         return self.film_id

# #put & get done
# class show(models.Model):
#     show_id = models.CharField(max_length=50, primary_key=True)
#     film = models.ForeignKey(film, on_delete=models.CASCADE, related_name='shows')
#     show_time = models.CharField(max_length=50)
#     screen_name = models.CharField(max_length=50)
#     is_blocked_covidseat = models.CharField(max_length=10)
#     is_covidtime = models.CharField(max_length=10)
#     show_date = models.CharField(max_length=50)
#     show_category_name = models.CharField(max_length=50)


#     def __str__(self):
#         return self.show_id
# # get & put done
# class theatre(models.Model):
#     theatre_id = models.CharField(max_length=50, primary_key=True)
#     theatre_location = models.CharField(max_length=100)
#     is_currently_tracking = models.CharField(max_length=50)

#     def __str__(self):
#         return self.theatre_id

# class show_theatre(models.Model):
#     theatre = models.ForeignKey(theatre, on_delete=models.CASCADE)
#     show = models.ForeignKey(show, on_delete=models.CASCADE , primary_key=True)
    

# def __str__(self):
#         return "%s %s" %(self.film_id,self.show_id) 
# # put & get done
# class data(models.Model):
    
#     data_id = models.AutoField(primary_key=True)
#     show = models.ForeignKey(show_theatre,on_delete=models.CASCADE)
#     price = models.CharField(max_length=500)
#     booked_seats = models.CharField(max_length=50)
#     available_seats = models.CharField(max_length=50)
#     total_seats = models.CharField(max_length=50)
#     last_modified = models.CharField(max_length=50)
    

#     def __str__(self):
#         return self.data_id





