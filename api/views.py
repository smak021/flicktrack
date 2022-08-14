import imp
from re import T
import re
from django.shortcuts import render
from pkg_resources import safe_extra
from rest_framework import status,generics
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, response
import requests
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from django.core import serializers
# from .models import ft_data, film_det, film_loc
from django.views.decorators.csrf import csrf_exempt
#from .serializers import dataserializer,filmserializer,filmlocserializer
from .models import show, track, film,status 
from .serializers import filmfilterserializer, showserializer, filmserializer, trackserializer,dataserializer,statusserializer


# Create your views here.


def home_pg(self):
    return HttpResponse('<h2>Hello</h2>')

# #REBUILD
# # Theatre GET & PUT
# @csrf_exempt
# def theatreList(request):
#     if request.method == 'GET':
#         location_data = theatre.objects.all()
#         serializer = theatreserializer(location_data, many = True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         putData = JSONParser().parse(request)
#         serializer = theatreserializer(data=putData)

#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data)

# # Single Film GET only
# @csrf_exempt
# def filmSingle(request,filmid):
#     if request.method == 'GET':
#         filmData =  film.objects.filter(film_id__exact = filmid)
#         serializer = filmserializer(filmData, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     if serializer.is_valid():
#         serializer.save()
#     return JsonResponse(serializer.data)

# # Data Table GET & PUT
# @csrf_exempt
# def filmData(request):
#     if request.method == 'GET':
#         filmData = data.objects.all()
#         serializer = dataNserializer(filmData, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         putData = JSONParser().parse(request)
#         serializer = dataNserializer(data=putData)
 
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data)
#     return JsonResponse(serializer.errors)


# # important: Main data linked with different tables only GET , PUT not working since connected
# @csrf_exempt
# def mainData(request):
#     dataa = data.objects.select_related('show')
#     if request.method == 'GET':
#         serializer = dataserializer(dataa, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data)
#     return JsonResponse(serializer.errors)

# #TESTING, Remove later
# class ReportApi(generics.RetrieveAPIView):
#     serializer_class = testserializer
#     queryset = film.objects.all()

# #Trying to read complete data with film ID
# @csrf_exempt
# def getMainData(request,filmid):
#     if request.method == 'GET':
#         gData = data.objects.filter(show_id__exact = filmid)
#         serializer = dataserializer(gData, many = True)
#         return JsonResponse(serializer.data, safe=False)

#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data)
#     return JsonResponse(serializer.errors)


# # Films GET & PUT
# @csrf_exempt
# def films(request):
#     if request.method == 'GET':
#         filmdata = film.objects.all().order_by('-release_date')
#         serializer = filmserializer(filmdata, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         putData = JSONParser().parse(request)
#         serializer = filmserializer(data=putData)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors)

# # Put film using film ID provided by BMS
# @csrf_exempt
# def filmlist(request,filmid):
#     try:
#         film_data = film.objects.get(film_id__exact=filmid)
#     except film.DoesNotExist:
#         if request.method == 'PUT':
#             putData = JSONParser().parse(request)
#             serializer = filmserializer(data=putData)

#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data)
#             return JsonResponse(serializer.errors)

#         elif request.method == 'GET':
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = filmserializer(film_data)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         pdata = JSONParser().parse(request)
#         serializer = filmserializer(film_data, data=pdata)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors)

#     elif request.method == 'DELETE':
#         film_data.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# # shows Get & put 
# @csrf_exempt
# def shows(request):
#     if request.method == 'GET':
#         showData = show.objects.all()
#         serializer = showNserializer(showData, many=True,context = {'isConnect':0})
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         putData = JSONParser().parse(request)
#         serializer = showNserializer(data=putData)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors)

# #showTheatre get & put
# @csrf_exempt
# def showTheatre(request):
#     if request.method == 'GET':
#         showTheatreData = show_theatre.objects.all()
#         serializer = showtheatreNserializer(showTheatreData, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         putData = JSONParser().parse(request)
#         serializer = showtheatreNserializer(data=putData)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors)

#New 30/7/2022


@csrf_exempt
def films(request):
    if request.method == 'GET':
        filmdata = film.objects.all().order_by('-release_date')
        serializer = filmserializer(filmdata, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = filmserializer(data=putData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def shows(request):
    if request.method == 'GET':
        showData = show.objects.all()
        serializer = showserializer(showData , many = True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = showserializer(data=putData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def statuss(request):
    if request.method == 'GET':
        statusData = status.objects.all()
        serializer = statusserializer(statusData , many = True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = statusserializer(data=putData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

@csrf_exempt
def tracks(request):
    if request.method == 'GET':
        trackData = track.objects.all()
        serializer = trackserializer(trackData , many = True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = trackserializer(data=putData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def putShow(request, showid, categoryname):
    try:
        showData = show.objects.get(show_id__exact = showid, category_name__exact = categoryname)
    except show.DoesNotExist:
        if request.method == 'PUT':
            putData = JSONParser().parse(request)
            serializer = showserializer(data= putData)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)   
    
    if request.method == 'GET':
        serializer = showserializer(showData)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        pdata = JSONParser().parse(request)
        serializer = showserializer(showData, data=pdata)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    elif request.method == 'DELETE':
        showData.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



# Put film using film ID provided by BMS
@csrf_exempt
def filmlist(request,filmid):
    try:
        film_data = film.objects.get(film_id__exact=filmid)
    except film.DoesNotExist:
        if request.method == 'PUT':
            putData = JSONParser().parse(request)
            serializer = filmserializer(data=putData)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = filmserializer(film_data)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        pdata = JSONParser().parse(request)
        serializer = filmserializer(film_data, data=pdata)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    elif request.method == 'DELETE':
        film_data.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ReportApi(generics.RetrieveAPIView):
    serializer_class = dataserializer
    queryset = film.objects.all()


class FilmfilterApi(generics.RetrieveAPIView):
    serializer_class = filmfilterserializer
    queryset = film.objects.all().order_by('-release_date')