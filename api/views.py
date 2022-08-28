from django.db.models import Sum,F
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db.models import FloatField
from rest_framework.decorators import api_view
from rest_framework import status,generics,views
from rest_framework.response import Response
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
        filmdata = film.objects.filter(film_status='active').order_by('-release_date')
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



#Update
@api_view(['GET', 'PUT'])
def snippet_detail(request, pk):
    try:
        snippet = film.objects.get(pk=pk)
    except snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = filmserializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = filmserializer(snippet, data=putData,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

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
        serializer = filmserializer(film_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     serializer.save(commit=False)
        #     return JsonResponse(serializer.data)
        # return JsonResponse(serializer.errors)

    elif request.method == 'DELETE':
        film_data.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ReportApi(generics.RetrieveAPIView):
    serializer_class = dataserializer
    queryset = film.objects.all()

@csrf_exempt
def singleFilm(request,filmid):
    if request.method == 'GET':
        filmdata = film.objects.filter(film_id = filmid)
        serializer = filmserializer(filmdata, many=True)
        return JsonResponse(serializer.data, safe=False)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


class TheatreData(views.APIView):
    def get(self,request,filmid):
        data={}
        filmname = film.objects.filter(film_id=filmid).first().full_name
        print(filmname)
        for row in show.objects.filter(film_id=filmid).order_by('theatre_code').values_list('theatre_code',flat=True).distinct():
            print(row)
            query = show.objects.filter(film_id=filmid, theatre_code=row)
            theatre_name = query.first().theatre_name
            theatre_location = track.objects.filter(theatre_code = row).first().loc_real_name
            number = query.values_list('show_id',flat=True).distinct().count()     
            test_booked = query.annotate(booked_seat=Cast('booked_seats', IntegerField())).aggregate(Sum('booked_seat'))
            test_amount = query.annotate(booked_seat=Cast('booked_seats', IntegerField()),amount = Cast('price',FloatField())).aggregate(total=Sum(F('booked_seat')*F('amount'),output_field=FloatField()))
            test_total = query.annotate(t_seat=Cast('total_seats', IntegerField())).aggregate(Sum('t_seat'))
            data[row] = {"name": filmname,'theatre_code':row,'theatre_name':theatre_name,'theatre_location':theatre_location.capitalize(),'shows':number,"booked_seats":test_booked['booked_seat__sum'],"total_seats":test_total["t_seat__sum"],'total_amount':test_amount["total"]}
        return Response(data)




class EndPoint(views.APIView):
    def get(self, request,filmid):
        data={}
        filmname = film.objects.filter(film_id=filmid).first().full_name
        print(filmname)
        for row in show.objects.filter(film_id=filmid).order_by('-show_date').values_list('show_date',flat=True).distinct():
            print(row)
            query = show.objects.filter(film_id=filmid, show_date=row)
            booked = query.annotate(booked_seat=Cast('booked_seats', IntegerField())).aggregate(Sum('booked_seat'))["booked_seat__sum"]
            amount = query.annotate(booked_seat=Cast('booked_seats', IntegerField()),amount = Cast('price',FloatField())).aggregate(total=Sum(F('booked_seat')*F('amount'),output_field=FloatField()))["total"]
            total = query.annotate(t_seat=Cast('total_seats', IntegerField())).aggregate(Sum('t_seat'))["t_seat__sum"]
            number = query.values_list('show_id',flat=True).distinct().count() 
            data[row] = {"name": filmname,'date':row,'shows':number,"booked_seats":booked,"total_seats":total,'total_amount':amount}
        return Response(data)


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
