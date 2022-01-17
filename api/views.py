from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, response
import requests
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .models import ft_data, film_det, film_loc
from django.views.decorators.csrf import csrf_exempt
from .serializers import dataserializer,filmserializer,filmlocserializer


# Create your views here.


def home_pg(self):
    return HttpResponse('<h2>Hello</h2>')



@csrf_exempt
def track_list(request):

    if request.method == 'GET':
        ftdata = ft_data.objects.all()
        serializer = dataserializer(ftdata, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = dataserializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

@csrf_exempt
def film_details(request, showid, showdate, filmid):
    try:
        #ftdata = ft_data.objects.get(pk=pk)
        ftdata = ft_data.objects.get(show_id__exact=showid, show_date__exact=showdate, film_id__exact=filmid)
        print("Hello")
    except ft_data.DoesNotExist:
        if request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = dataserializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = dataserializer(ftdata)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = dataserializer(ftdata, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    elif request.method == 'DELETE':
        ftdata.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def film_list(request):

    if request.method == 'GET':
        filmdata = film_det.objects.all()
        serializer = filmserializer(filmdata, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = filmserializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

@csrf_exempt
def put_film_list(request, filmid, filmloc):
    try:
        pfilmdata = film_det.objects.get(film_id__exact=filmid, film_loc__exact=filmloc)
    except film_det.DoesNotExist:
        if request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = filmserializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = filmserializer(pfilmdata)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = filmserializer(pfilmdata, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    elif request.method == 'DELETE':
        pfilmdata.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def loc_det(request):

    if request.method == 'GET':
        ftdata = film_loc.objects.all()
        serializer = filmlocserializer(ftdata, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = filmlocserializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def single_film_list(request, filmid):
    if request.method == 'GET':
        ftdata = ft_data.objects.filter(film_id__exact=filmid)
        serializer = dataserializer(ftdata, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def get_single_film_list(request, filmid):
    if request.method == 'GET':
        ftdata = film_det.objects.filter(film_id__exact=filmid)
        serializer = filmserializer(ftdata, many=True)
        return JsonResponse(serializer.data, safe=False)
