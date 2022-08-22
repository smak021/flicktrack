from django.contrib import admin
from django.urls import path
from api.views import filterfilm, films, tracks, shows, filmlist, putShow,ReportApi,statuss


urlpatterns = [
  path('status/',statuss),
  path('putshow/<str:showid>/<str:categoryname>/',putShow),
  path('films/',films),
  path('putfilm/<str:filmid>/',filmlist),
  path('shows/',shows),
  path('tracks/',tracks),
  # path('theatrenshows/',showTheatre),
  path('data/<pk>/',ReportApi.as_view()),
  path('filmfilter/',filterfilm),
]