from cmath import log
from distutils.log import Log
from enum import unique
from attr import field
from rest_framework import serializers
# from .models import ft_data,film_det,film_loc
from .models import film,show,track,status

# New 30/7/2022

class filmserializer(serializers.ModelSerializer):

    class Meta:
        model = film
        fields = '__all__'

class showserializer(serializers.ModelSerializer):

    class Meta:
        model = show
        fields = '__all__'

    def create(self, validated_data):
        tag = validated_data.pop('film')
        tag_instance, created = film.objects.get_or_create(film_id=tag)
        article_instance = show.objects.create(**validated_data, film=tag_instance)
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
        shows = show.objects.filter(film_id = obj.film_id)
        return showserializer(shows, many = True).data

        
# #REBUILD 
# #test
# class testserializer(serializers.ModelSerializer):
#     # show_id = serializers.CharField(read_only=True)
#     shows = serializers.SerializerMethodField()
#     class Meta:
#         model = film
#         fields = '__all__'
    
#     def get_shows(self, obj):
#         shows = show.objects.filter(film_id = obj.film_id)
#         return testShowSerializer(shows,many=True,context = {"show_id":shows}).data


#     #shows = showserializer(many=True)
#     class Meta:
#         model = film
#         fields = ['film_id', 'film_name', 'cover_url', 'release_date', 'film_story', 'film_genre', 'film_censor', 'film_duration']


# class showNserializer(WritableNestedModelSerializer,serializers.ModelSerializer):
#     # film_id=serializers.SlugRelatedField(many=False, read_only=True, slug_field='film_id')
#     class Meta:
#         model = show
#         fields = ['show_id','show_category_name','film', 'show_time', 'screen_name', 'is_blocked_covidseat', 'is_covidtime', 'show_date']
#     def create(self, validated_data):
#         tag = validated_data.pop('film')
#         tag_instance, created = film.objects.get_or_create(film_id=tag)
#         article_instance = show.objects.create(**validated_data, film=tag_instance)
#         return article_instance

# class dataNserializer( serializers.ModelSerializer):
#     class Meta:
#         model = data
#         fields = ['data_id','show', 'price', 'booked_seats', 'available_seats', 'total_seats', 'last_modified']
#     def create(self, validated_data):
#         tag = validated_data.pop('show')
#         tag_instance, created = show_theatre.objects.get_or_create(show_id=tag)
#         article_instance = data.objects.create(**validated_data, show=tag_instance)
#         return article_instance

# class showtheatreNserializer(serializers.ModelSerializer):
#     # theatre=serializers.SlugRelatedField(many=False, read_only=True, slug_field='theatre_id')
#     class Meta:
#         model = show_theatre
#         fields = ['theatre', 'show']

#     def create(self, validated_data):
#         show_id = validated_data.pop('show')
#         theatre_id = validated_data.pop('theatre')
#         # theatre_instance = serializers.PrimaryKeyRelatedField(theatre_id= theatre_id)
#         theatre_instance, created = theatre.objects.get_or_create(theatre_id = theatre_id)
#         # theatre_instance=serializers.SlugRelatedField(many=False, read_only=True, slug_field='theatre_id')
#         show_instance, created = show.objects.get_or_create(show_id=show_id)
#         article_instance = show_theatre.objects.create(**validated_data, show=show_instance,theatre = theatre_instance)
#         return article_instance


# class theatreserializer(serializers.ModelSerializer):
#     class Meta:
#         model = theatre
#         fields = ['theatre_id', 'theatre_location', 'is_currently_tracking']


# #connected
# class showserializer(serializers.ModelSerializer):
#     film = filmserializer(many =False)
#     # film=serializers.SlugRelatedField(many=False, read_only=True, slug_field='film_id')
#     class Meta:
#         model = show
#         unique_together = ()
#         fields = ['show_id','show_category_name', 'film', 'show_time', 'screen_name', 'is_blocked_covidseat', 'is_covidtime', 'show_date']


# class showtheatreserializer(serializers.ModelSerializer):
    
#     show = showserializer(many = False)
#     class Meta:
#         model = show_theatre
#         fields = ['theatre', 'show']

# class dataserializer( serializers.ModelSerializer):
#     show = showtheatreserializer(many = False)
#     class Meta:
#         model = data
#         fields = ['data_id','show', 'show_id', 'price', 'booked_seats', 'available_seats', 'total_seats', 'last_modified']


# #test
# class testserializer(serializers.ModelSerializer):
#     # show_id = serializers.CharField(read_only=True)
#     shows = serializers.SerializerMethodField()
#     class Meta:
#         model = film
#         fields = '__all__'
    
#     def get_shows(self, obj):
#         shows = show.objects.filter(film_id = obj.film_id)
#         return testShowSerializer(shows,many=True,context = {"show_id":shows}).data

# class testShowSerializer(serializers.ModelSerializer):
#     # data = serializers.SerializerMethodField()
#     # showT = dataNserializer()
#     class Meta:
#         model = show
#         fields = '__all__'
    
#     # def get_data(self,obj):
#     #     show_idd = self.context.get("show_id")
#     #     dataa = data.objects.filter(showT = show_idd)
#     #     return dataNserializer(dataa, many = False).data

   

    
