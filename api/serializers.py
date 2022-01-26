from rest_framework import serializers
from .models import ft_data,film_det,film_loc


class dataserializer(serializers.ModelSerializer):
    class Meta:
        model = ft_data
        fields = ['film_name','film_id','theatre_id','category_name','screen_name','show_id','available_seat','total_seat','booked_seat','Show_time','show_date','price','film_loc','last_modified']

class filmserializer(serializers.ModelSerializer):
    class Meta:
        model = film_det
        fields= ['film_name','film_length','film_genre','film_story','film_censor','film_real_name','film_id','release_date','image_url','film_loc']

class filmlocserializer(serializers.ModelSerializer):
    class Meta:
        model = film_loc
        fields= ['film_location','venue_id']



