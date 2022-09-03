from rest_framework import serializers
from .models import film,show,track,status,mdata

# New 30/7/2022

class filmserializer(serializers.ModelSerializer):

    class Meta:
        model = film
        fields = '__all__'

class mdataserializer(serializers.ModelSerializer):

    class Meta:
        model = mdata
        fields = '__all__'

    def create(self, validated_data):
        tag = validated_data.pop('film')
        tag_instance, created = film.objects.get_or_create(film_id=tag)
        article_instance = mdata.objects.create(**validated_data, film=tag_instance)
        return article_instance


class statusserializer(serializers.ModelSerializer):
    film = filmserializer(many = False)
    class Meta:
        model = status 
        fields = '__all__'    

class trackserializer(serializers.ModelSerializer):

    class Meta:
        model = track 
        fields = '__all__'


class dataserializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()
    class Meta:
        model= film
        fields = '__all__' 

    def get_show(self,obj):
        shows = mdata.objects.filter(film_id = obj.film_id).order_by('-show_date')
        return mdataserializer(shows, many = True).data

class filmfilterserializer(serializers.ModelSerializer):

    class Meta:
        model = film
        fields = ['film_id','film_name','cover_url','full_name','release_date']

class showserializer(serializers.ModelSerializer):

    class Meta:
        model = show
        fields = '__all__'

 