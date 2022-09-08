from django.contrib import admin
from django.urls import path
from api.views import EndPoint, filterData, getShow,getbytheatre,putShow,nw_putData,snippet_detail, filterfilm, films, singleFilm, topweek, tracks, data, filmlist, putData,ReportApi,statuss


urlpatterns = [
  path('status/',statuss),
  path('putdata/<str:showid>/<str:categoryname>/',putData),
  path('porgdata/<str:theatrecode>/<str:date>/<str:filmid>/',nw_putData),
  path('putshow/<str:showid>/',putShow),
  path('getshows/<str:theatrecode>/<str:date>/<str:filmid>/',getShow),
  path('topweek/<str:date1>/<str:date2>/',topweek),
  path('films/',films),
  # path('testfilms/',FilmListView.as_view()),
  path('upfilm/<str:pk>',snippet_detail),
  path('putfilm/<str:filmid>/',filmlist),
  path('shows/',data),
  path('tracks/',tracks),
  path('data/<pk>/',ReportApi.as_view()),
  path('getData/<str:filmid>/',filterData),
  path('filmfilter/',filterfilm),
  path('getbydate/<str:filmid>/',EndPoint.as_view()),
  path('getbytheatre/<str:filmid>/',getbytheatre),
  path('getfilm/<str:filmid>/',singleFilm),
]