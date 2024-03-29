from cmath import log
import math
from datetime import datetime, timedelta
import pytz
from urllib import response
from django.db.models.functions import Cast
from django.db.models import IntegerField,Q,FloatField, Sum,F
from rest_framework.decorators import api_view
from rest_framework import generics,views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import requests
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from .models import mdata, track, film,status,show
from .serializers import filmfilterserializer,showserializer ,mdataserializer, filmserializer, trackserializer,dataserializer,statusserializer
import pymongo
from pymongo.errors import BulkWriteError
from bson import json_util, ObjectId
from bson.son import SON
import os
from pathlib import Path
import dj_database_url


def Mongoconnect():
    client = pymongo.MongoClient(os.environ.get('DATABASE_HOST'))
        #Define Db Name
    dbname = client[os.environ.get('DATABASE_NAME')]
    return dbname


def topfivepipeline(condition):
    pipeline = [ 
        {
        "$lookup":{
                "from": "api_film",       
                "localField": "film_id",  
                "foreignField": "film_id", 
                "as": "film"         
            }
        },
          {   "$unwind":"$film" },
        {
            "$project":
            {
                'film._id':0,
                'film_film_status':0,
                'film.tn_code':0,
                'film.ptm_code':0,
                'film.priority':0,
                'highlight':0,
                'other_lang_code':0,
                'film.film_story':0
            }
        },
        {
            "$match":condition
        },
        {
            "$group":{
                "_id":{"film_id":"$film_id","show_date":"$show_date"},
                "film":{"$first":"$film"},
                "total":{"$sum":{'$toDouble':"$price"}},
            }
        },
        {
            "$group":{
                "_id":"$_id.film_id",
                "film":{"$first":"$film"},
                "total":{"$sum":{'$toDouble':"$total"}},
                "rows":{"$push":{"date":"$_id.show_date","amount":"$total"}},
            }
        },
        {
            "$project":{"_id":0}
        },
        {
            "$sort":SON([("total", -1)])
        },
        {
            "$limit":5
        }
    ]
    return pipeline

# PyMongo
# GET
@csrf_exempt
def pytest(request,filmid):
    if request.method == 'GET':
        data=[]
        data2=[]
        
        dbname = Mongoconnect()
        
        #Define Collection
        collection = dbname['api_mdata']
        pipeline1 = [
            {
        "$lookup":{
            "from": "api_track",       
            "localField": "theatre_code",  
            "foreignField": "theatre_code", 
            "as": "theatre_location"         
        }
    },
    {   "$unwind":"$theatre_location" },
            {
                "$match": {"film_id":filmid}
                },
               
            {
                "$group":{"_id":"$theatre_code","theatre_location":{"$first":"$theatre_location.loc_real_name"},"theatre_name":{"$first":"$theatre_name"},"show_count":{"$sum":{'$toInt':"$show_count"}},"booked_seats":{"$sum":{'$toInt':"$booked_seats"}},"total_seats":{"$sum":{'$toInt':"$total_seats"}},"available_seats":{"$sum":{'$toInt':"$available_seats"}},"price":{"$sum":{'$toDouble':"$price"}}}
                },
                {
                    "$project":{
                        "_id":0,
                        "theatre_code":"$_id",
                        "theatre_location":1,
                        "theatre_name":1,
                        "show_count":1,
                        "booked_seats":1,"total_seats":1,
                        "available_seats":1,
                        "price":1

                    }
                },
                {
                    "$sort":SON([("price", -1)])
                }
        ]
        pipeline2 = [
            {
                "$match": {"film_id":filmid}
                },
            {
                "$group":{"_id":"$show_date","film": { "$first": "$film_id"},"shows":{"$sum":{'$toInt':"$show_count"}},"booked_seats":{"$sum":{'$toInt':"$booked_seats"}},"total_seats":{"$sum":{'$toInt':"$total_seats"}},"available_seats":{"$sum":{'$toInt':"$available_seats"}},"total_amount":{"$sum":{'$toDouble':"$price"}},"last_modified":{"$first":"$last_modified"}}
                },
                {
                    "$project":{
                        "_id": 0,
                        "date":"$_id",
                        "film": 1,
                        "shows": 1,
                        "booked_seats": 1,
                        "total_seats": 1,
                        "available_seats": 1,
                        "total_amount": 1,
                        "last_modified": 1
                    }
                },
                {
                    "$sort":SON([("date", 1)])
                }
        ]
        
        dateData = collection.aggregate(pipeline2)
        theatreData = collection.aggregate(pipeline1)
        data = list(dateData)
        data2 = list(theatreData)
        page1 = json.loads(json_util.dumps(data))
        page2 = json.loads(json_util.dumps(data2))
        final = {"date":page1,"theatre":page2}
    return JsonResponse(final,safe=False)

@api_view(['GET'])
def getFilms(request):
    dbname = Mongoconnect()
    collection = dbname['api_film']
    cursor = collection.find({"film_status":{"$ne":'inactive'}},{"_id":0}).sort([("highlight",pymongo.DESCENDING),("release_date",pymongo.DESCENDING),("priority",pymongo.DESCENDING)])
    data = list(cursor)
    data_json = json.loads(json_util.dumps(data))
    return JsonResponse(data_json,safe=False)


@api_view(['GET'])
def getSingleFilm(request,filmid):
    dbname = Mongoconnect()
    collection = dbname['api_film']
    cursor = collection.find_one({"film_id":filmid})
    data_json = json.loads(json_util.dumps(cursor))
    return JsonResponse(data_json,safe=False)

@api_view(['GET'])
def getShows(request,theatrecode,date,filmid): 
    dbname = Mongoconnect()
    collection = dbname['api_show']
    collection2 = dbname['api_film']
    query = collection2.find_one({'film_id':filmid},{'_id':0,'release_date':1})
    data_json = json.loads(json_util.dumps(query))
    release_date=data_json['release_date']
    relDate = datetime.strptime(release_date,'%Y-%m-%d')
    todDate = datetime.strptime(date,'%Y%m%d')
    res = relDate-todDate
    if(res.days>0):
        query = collection.find({'film_id':filmid,'show_date':{'$gte':date},'theatre_code':theatrecode},{'_id':0})
    else:
        query = collection.find({'film_id':filmid,'show_date':date,'theatre_code':theatrecode},{'_id':0})
    data_json = json.loads(json_util.dumps(query))
    return JsonResponse(data_json,safe=False) 

@api_view(['GET'])
def getTheaters(request):
    dbname = Mongoconnect()
    collection = dbname['api_track']
    cursor = collection.find({},{'_id':0}).sort('theatre_code')
    data = list(cursor)
    data_json = json.loads(json_util.dumps(data))
    return JsonResponse(data_json,safe=False)



# Add film Done
# Add Mdata Done
# Add shows pending(trying for bulk insert with update)

# POST/PUT
# Mdata
@api_view(['PUT'])
def putmData(request,theatrecode,date,filmid):
    putData = JSONParser().parse(request)
    dbname = Mongoconnect()
    collection = dbname['api_mdata']
    cursor = collection.update({"show_date":date,"theatre_code":theatrecode,'film_id':filmid},putData,upsert=True)
    return JsonResponse({"status":"Completed"},safe=False)

@api_view(['PUT'])
def putFilm(request,filmid):
    putData = JSONParser().parse(request)
    dbname = Mongoconnect()
    collection = dbname['api_test']
    msg=""
    try:
        cursor = collection.update({'film_id':filmid},putData,upsert=True)
    except:
        msg="Error"
        print("Error adding film")
    else:
        msg="Success"
        print("Film Added")
    return JsonResponse({"status":msg},safe=False)


# Shows
@api_view(['GET'])
def topfive(request):
    # find dates
    dateFormat = '%Y%m%d'
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    day = datetime_NY.weekday()
    if(day<3):
        offset = 4 + day 
    else:
        offset = day - 3
    datetwo = (datetime_NY - timedelta(days=offset))
    dateone = (datetwo-timedelta(days=6)).strftime(dateFormat)
    datetwo = datetwo.strftime(dateFormat)
    # //
    dbname = Mongoconnect()
    collection = dbname['api_mdata']
    pipeline = topfivepipeline({"show_date":{"$lte":datetwo,"$gte":dateone}})
    weekly = collection.aggregate(pipeline)
    pipeline = topfivepipeline({})
    total = collection.aggregate(pipeline)
    data = list(weekly)
    data2 = list(total)
    data_json = json.loads(json_util.dumps(data))
    data2_json = json.loads(json_util.dumps(data2))
    final={'dates':{'from':dateone,'to':datetwo},'weekly':data_json,'total':data2_json}
    return JsonResponse(final,safe=False)

#  value = {"film_id":item,"total":query_sum,"film_name":film_name,"cover_pic":film_cover,"release_date":release_date}
@api_view(['PUT'])
def putShows(request):
    print(request.user)
    print(request.auth)
    putData = JSONParser().parse(request)
    dbname = Mongoconnect()
    collection=dbname['api_test']
    
    msg=""
    try:
        cursor = collection.insert_many(putData,ordered=False)
    except BulkWriteError as ex:
        # print()
        data = ex.details['writeErrors']
        # print(data)
        for row in data:
            # id = {"Name":row}
            msg = "Insert error"
            # print(ex.details)
            data = row["op"]
            id = {"Name":data["Name"]}
            print(id)
            print(data)
            try:
                update = collection.update_one(id,{"$set":data},upsert=True)
            except Exception as ex:
                msg = ex.args
            else:
                msg="Success"
        print ("Error")
    except:
        msg="Error"
    else:
        msg="Success"
    return JsonResponse({"status":msg},safe=False)
# Put Single
# Put bulk
# Get shows with date constrains


# DELETE



# PyMongo End
# Create your views here.


def home_pg(self):
    return HttpResponse('<h2>Welcome</h2>')


#New 30/7/2022


@csrf_exempt
def films(request):
    if request.method == 'GET':
        filmdata = film.objects.filter(~Q(film_status='inactive')).order_by('-highlight','-release_date','-priority')
        serializer = filmserializer(filmdata, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = filmserializer(data=putData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

# Pagination
# class FilmListView(ListAPIView):
#     queryset = film.objects.filter(~Q(film_status='inactive')).order_by('-release_date')
#     serializer_class = filmserializer
#     pagination_class = PageNumberPagination


@csrf_exempt
def filterData(request,filmid):
    if request.method == 'GET':
        showData = mdata.objects.filter(film_id = filmid)
        serializer = mdataserializer(showData , many = True)
        return JsonResponse(serializer.data, safe=False)
    

@csrf_exempt
def data(request):
    if request.method == 'GET':
        showData = mdata.objects.all()
        serializer = mdataserializer(showData , many = True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        putData = JSONParser().parse(request)
        serializer = mdataserializer(data=putData)

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
        trackData = track.objects.all().order_by('theatre_code')
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
def nw_putData(request,theatrecode, date,filmid):
    try:
        showData = mdata.objects.get(theatre_code__exact = theatrecode, show_date__exact = date,film_id__exact = filmid)
    except mdata.DoesNotExist:
        if request.method == 'PUT':
            putData = JSONParser().parse(request)
            serializer = mdataserializer(data= putData)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return JsonResponse({'Error': 'Not Found'}, status=401)   
    
    if request.method == 'GET':
        serializer = mdataserializer(showData)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        pdata = JSONParser().parse(request)
        serializer = mdataserializer(showData, data=pdata)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    elif request.method == 'DELETE':
        showData.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)




@csrf_exempt
def putData(request, showid, categoryname):
    try:
        showData = mdata.objects.get(show_id__exact = showid, category_name__exact = categoryname)
    except mdata.DoesNotExist:
        if request.method == 'PUT':
            putData = JSONParser().parse(request)
            serializer = mdataserializer(data= putData)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)   
    
    if request.method == 'GET':
        serializer = dataserializer(showData)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        pdata = JSONParser().parse(request)
        serializer = mdataserializer(showData, data=pdata)

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


@api_view(['GET'])
def getbytheatre(request,filmid):
        arr=[]
        url =requests.get('https://flicktracks.herokuapp.com/api/getData/'+filmid+'/?format=json')
        print(url)
        data = json.loads(url.text)
        uni = sorted(set(dic['theatre_code'] for dic in data))
        # print(uni) 
        for item in uni:
            # print(item)
            dsf = [val for val in data if val['theatre_code'] == item]
            total=0
            booked=0
            avail=0
            price=0
            indv = []
            show_count=0
            for item2 in dsf:
                total += int(item2['total_seats'])
                avail += int(item2['available_seats']) 
                booked += int(item2['booked_seats'])
                price += float(item2['price'])
                show_count += int(item2['show_count'])
                # indv.append({'show_date':item2['show_date'],'show_count':item2['show_count'],'total':item2['total_seats'],'avail':item2['available_seats'],'booked':item2['booked_seats'],'price':item2['price']})

            # print(dsf)
            nwdata = {'show_count': show_count, 'category_name': dsf[0]['category_name'], 'price': math.floor(price), 'booked_seats': booked, 'available_seats': avail, 'total_seats': total, 'theatre_code': item, 'theatre_location': dsf[0]['theatre_location'], 'theatre_name': dsf[0]['theatre_name'], 'last_modified': dsf[0]['last_modified'], 'film': dsf[0]['film'],'rows':indv}
            arr.append(nwdata)
        return Response(arr)


class EndPoint(views.APIView):
    def get(self, request,filmid):
        theatre_test={}
        darr=[]
        tarr=[]
        url = mdata.objects.filter(film_id = filmid)
        uni = url.order_by('show_date').values_list('show_date',flat=True).distinct()
        for item in uni.iterator(): 
            query = url.filter(show_date=item)
            total=0
            booked=0
            avail=0
            price=0
            show_count=0
            for it in query.iterator():
                total += int(it.total_seats)
                avail += int(it.available_seats) 
                booked += int(it.booked_seats)
                price += float(it.price)
                show_count += int(it.show_count)
                location = track.objects.filter(theatre_code=it.theatre_code).first().loc_real_name
                if it.theatre_code in theatre_test:
                    theatre_test[it.theatre_code]['total_seats']=theatre_test[it.theatre_code]['total_seats']+int(it.total_seats)
                    theatre_test[it.theatre_code]['show_count']=theatre_test[it.theatre_code]['show_count']+int(it.show_count)
                    theatre_test[it.theatre_code]['booked_seats']=theatre_test[it.theatre_code]['booked_seats']+int(it.booked_seats)
                    theatre_test[it.theatre_code]['available_seats']=theatre_test[it.theatre_code]['available_seats']+int(it.available_seats)
                    theatre_test[it.theatre_code]['price']=theatre_test[it.theatre_code]['price']+math.floor(float(it.price))
                    theatre_test[it.theatre_code]['last_modified']=it.last_modified
                else:
                    theatre_test[it.theatre_code]={'show_count':int(it.show_count),'total_seats':int(it.total_seats),'booked_seats':int(it.booked_seats),'available_seats': int(it.available_seats) ,'price': math.floor(float(it.price)),'theatre_code': it.theatre_code, 'theatre_location': location, 'theatre_name':it.theatre_name}
            nwdata = {'shows': show_count,'total_amount': math.floor(price), 'booked_seats': booked, 'available_seats': avail, 'total_seats': total, 'date': item, 'last_modified': it.last_modified}
            darr.append(nwdata)
        data = {'film':filmid,'theatre':theatre_test.values(),'date':darr}
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


# shows
@csrf_exempt
def putShow(request,showid):
    try:
        showData = show.objects.get(show_id__exact = showid)
    except show.DoesNotExist:
        if request.method == 'PUT':
            putData = JSONParser().parse(request)
            serializer = showserializer(data= putData)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)

        elif request.method == 'GET':
            return JsonResponse({'error':'Not Found'}, status=401)   
    
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

# @csrf_exempt
# def getShows(request,theatrecode, date,filmid):
#     if request.method == 'GET':
#         queryset = show.objects.filter(theatre_code__exact = theatrecode, show_date__gte = date,film_id__exact=filmid)
#         serializer = showserializer(queryset , many = True)
#         return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def getShow(request,theatrecode, date,filmid):
    release_date = film.objects.filter(film_id__exact = filmid).first().release_date
    relDate = datetime.strptime(release_date,'%Y-%m-%d')
    todDate = datetime.strptime(date,'%Y%m%d')
    res = relDate-todDate
    if(res.days > 0):
        queryset = show.objects.filter(theatre_code__exact = theatrecode, show_date__gte = date,film_id__exact=filmid)
    else:
        queryset = show.objects.filter(theatre_code__exact = theatrecode, show_date__exact = date,film_id__exact=filmid)
    serializer = showserializer(queryset , many = True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def clear_data(request):
    dateFormat = '%Y%m%d'
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    today = datetime_NY.strftime(dateFormat)
    try:
        query = show.objects.filter(show_date__lt = today).delete()
        return JsonResponse({'Result':'Successfully completed'}, status=200)
    except:
        return Response({'Result':'Not found'},status=404)

@api_view(['GET'])
def topweek(request,type):
    dateFormat = '%Y%m%d'
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    if(type == 1):
        day = datetime_NY.weekday()
        if(day<3):
            offset = 4 + day 
        else:
            offset = day - 3
        datetwo = (datetime_NY - timedelta(days=offset))
        dateone = (datetwo-timedelta(days=6)).strftime(dateFormat)
        datetwo = datetwo.strftime(dateFormat)
    elif(type == 0):
        dateone = film.objects.all().order_by('release_date').first().release_date
        read_date = datetime.strptime(dateone,'%Y-%m-%d').strftime('%Y%m%d')
        dateone = read_date
        datetwo = datetime_NY.strftime(dateFormat)
    
    if(type!=3):    
        dict_data = {}
        final_data={}
        arr=[]
        films = mdata.objects.filter(show_date__gte = dateone, show_date__lte = datetwo).values_list('film_id',flat=True).distinct()
        # query_s = mdata.objects.filter(show_date__gte = dateone, show_date__lte = datetwo,film_id__in = films).order_by('film_id')

        for item in films:
            fildata = film.objects.filter(film_id__exact = item).first()
            film_name = fildata.full_name
            film_cover = fildata.cover_url
            release_date = fildata.release_date
            query_sum = mdata.objects.filter(show_date__gte = dateone, show_date__lte = datetwo,film_id = item).order_by('film_id').annotate(pri = Cast('price',FloatField())).aggregate(total_price=Sum(F('pri'),output_field=IntegerField()))['total_price']
            value = {"film_id":item,"total":query_sum,"film_name":film_name,"cover_pic":film_cover,"release_date":release_date}
            arr.append(value)
        dict_data = arr
        dict_data = sorted(dict_data, key=lambda x:x['total'],reverse=True)[:5]
        topdata=[]
        for item2 in dict_data:     
            for row in mdata.objects.filter(show_date__gte = dateone, show_date__lte = datetwo,film_id=item2['film_id']).order_by('-show_date').values_list('show_date',flat=True).distinct():
                    query = mdata.objects.filter(film_id=item2['film_id'], show_date=row)
                    amount = query.annotate(booked_seat=Cast('booked_seats', IntegerField()),amount = Cast('price',FloatField())).aggregate(total=Sum('amount',output_field=IntegerField()))["total"]
                    topdata.append({"film_id": item2['film_id'],'date':row,'total_amount':amount})
        final_data = {"from":dateone,"to":datetwo,"topdata":topdata,"toptotal":dict_data}       
          
        # print(topfive)
        # data = mdata.objects.filter(show_date__gte = date1, show_date__lte = date2,film_id__in = topfive).order_by('film_id','show_date')
    elif(type == 3):
        datetwo = datetime_NY.strftime(dateFormat)
        dict_data = {}
        final_data={}
        arr=[]
        films = mdata.objects.filter(show_date = datetwo).values_list('film_id',flat=True).distinct()
        # query_s = mdata.objects.filter(show_date__gte = dateone, show_date__lte = datetwo,film_id__in = films).order_by('film_id')
# 
        for item in films:
            fildata = film.objects.filter(film_id__exact = item).first()
            film_name = fildata.full_name
            film_cover = fildata.cover_url
            release_date = fildata.release_date
            query_sum = mdata.objects.filter(show_date = datetwo,film_id = item).order_by('film_id').annotate(pri = Cast('price',FloatField())).aggregate(total_price=Sum(F('pri'),output_field=IntegerField()))['total_price']
            value = {"film_id":item,"total":query_sum,"film_name":film_name,"cover_pic":film_cover,"release_date":release_date}
            arr.append(value)
        dict_data = arr
        dict_data = sorted(dict_data, key=lambda x:x['total'],reverse=True)[:5]
        final_data = {"to":datetwo,"toptotal":dict_data}
    return Response(final_data)
    # serializer = mdataserializer(data,many=True)
    # return JsonResponse(serializer.data,safe=False)
