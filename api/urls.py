from django.contrib import admin
from django.urls import path
from api.views import EndPoint, TheatreData,snippet_detail, filterfilm, films, singleFilm, tracks, shows, filmlist, putShow,ReportApi,statuss


urlpatterns = [
  path('status/',statuss),
  path('putshow/<str:showid>/<str:categoryname>/',putShow),
  path('films/',films),
  path('upfilm/<str:pk>',snippet_detail),
  path('putfilm/<str:filmid>/',filmlist),
  path('shows/',shows),
  path('tracks/',tracks),
  path('data/<pk>/',ReportApi.as_view()),
  path('filmfilter/',filterfilm),
  path('getbydate/<str:filmid>/',EndPoint.as_view()),
  path('getbytheatre/<str:filmid>/',TheatreData.as_view()),
  path('getfilm/<str:filmid>/',singleFilm),
]