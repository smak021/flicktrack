from django.contrib import admin
from django.urls import path
#from api.views import get_location,film_details,get_single_film_list, home_pg, track_list, film_list, put_film_list,loc_det,single_film_list
#from api.views import track,loc_det
from api.views import films, tracks, shows, filmlist, putShow,ReportApi,statuss
# from api.views import ReportApi,getMainData,theatreList, filmSingle, filmData, mainData, films, filmlist, shows, showTheatre

urlpatterns = [
  # path('theatres/',theatreList),
  # path('getfilm/<str:filmid>/',filmSingle),
  # path('data/',filmData),
  # path('complete/',mainData),
  # path('complete/<str:filmid>',getMainData),
  path('status/',statuss),
  path('putshow/<str:showid>/<str:categoryname>/',putShow),
  path('films/',films),
  path('putfilm/<str:filmid>/',filmlist),
  path('shows/',shows),
  path('tracks/',tracks),
  # path('theatrenshows/',showTheatre),
  path('data/<pk>/',ReportApi.as_view())
]