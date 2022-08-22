from re import T
from django.shortcuts import render
from pkg_resources import safe_extra
from rest_framework import status,generics
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import show, track, film,status 
from .serializers import filmfilterserializer, showserializer, filmserializer, trackserializer,dataserializer,statusserializer


# Create your views here.


def home_pg(self):
    return HttpResponse('<h2>Hello</h2>')


#New 30/7/2022


@csrf_exempt
def films(request):
    if request.method == 'GET':
        filmdata = film.objects.filter(status='active').order_by('-release_date')
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


@csrf_exempt
def filterfilm(request):
    if request.method == 'GET':
        queryset = film.objects.all().order_by('-release_date')
        serializer = filmfilterserializer(queryset , many = True)
        return JsonResponse(serializer.data, safe=False)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
