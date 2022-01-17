from django.contrib import admin
from django.urls import path, include
from api.views import film_details,get_single_film_list, home_pg, track_list, film_list, put_film_list,loc_det,single_film_list

urlpatterns = [
    path('', home_pg),
    path('getdata/', track_list ),
    path('getfilmdata/', film_list),
    path('getlocdata/', loc_det),
    path('getfilmdata/<str:filmid>/<filmloc>/', put_film_list),
    path('getfilmdata/<str:filmid>/', get_single_film_list),
    path('getdata/<str:filmid>/', single_film_list),
    path('gufilm/<str:showid>/<str:showdate>/<str:filmid>/', film_details ),
]