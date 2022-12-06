import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import *
from .serializers import FavouritesSerializer
from spotdraft_test.settings import MOVIES_URL,PLANETS_URL

# Create your views here.

class PlanetsList(APIView):
    url = PLANETS_URL
    """
    API for returning planets list.
    must return : name, created, updated, url & is_favourite fields
    """
    def get(self,request):
        # getting query params
        query = request.query_params.get('search')
        page = request.query_params.get('page',1)
        user_id = request.headers.get('UserId')
        page = int(page)
        self.url+=f'?page={page}'
        add_params = ''
        if query:
            # returns actual name for querying
            query = get_query_name(query,obj_type="Planets")
            add_params=f'&search={query}'
            self.url+=add_params
        response = requests.get(self.url)
        try: 
            response = response.json()
            # Changing prev and next page urls to our wrapper url
            if response.get('next'):
                response['next']=str(request.build_absolute_uri())+f'?page={int(page)+1}{add_params}'
            if response.get('prev'):
                response['prev']=str(request.build_absolute_uri())+f'?page={int(page)-1}{add_params}'

            # getting formatted resukts with is_favourite key and updating api result
            response_data= get_formatted_data(obj_type="Planets",results=response['results'],user_id=user_id)
            response['results'] = response_data
            return Response(responsedata(True, "Planest List",response),status=status.HTTP_200_OK)
        except Exception as e:
            error = str(e)
            return Response(responsedata(False, error),status=status.HTTP_400_BAD_REQUEST)



class MoviesList(APIView):
    """
    API for returning movies list
    must return : title, release_date, created, updated, url and is_favourite
    """
    url = MOVIES_URL
    def get(self,request):
        # getting query params
        query = request.query_params.get('search')
        page = request.query_params.get('page',1)
        user_id = request.headers.get('UserId')
        page = int(page)

        self.url+=f'?page={page}'
        add_params = ''
        if query:
            # returns actual name for querying
            query = get_query_name(query,obj_type='Movies')
            add_params=f'&search={query}'
            self.url+=add_params
        
        response = requests.get(self.url)
        try: 
            response = response.json()
            # Changing prev and next page urls to our wrapper url
            if response.get('next'):
                response['next']=str(request.build_absolute_uri())+f'?page={int(page)+1}{add_params}'
            if response.get('prev'):
                response['prev']=str(request.build_absolute_uri())+f'?page={int(page)-1}{add_params}'

            # getting formatted results with is_favourite key and updating api result
            response_data= get_formatted_data(obj_type="Movies  ",results=response['results'],user_id=user_id)
            response['results'] = response_data
            return Response(responsedata(True, "Movies List",response),status=status.HTTP_200_OK)
        except Exception as e:
            error = str(e)
            return Response(responsedata(False, error),status=status.HTTP_400_BAD_REQUEST)


class FavouritesApi(APIView):
    """
    API for fetching from and adding data to favourites.
    """

    def get(self,request,pk=None):
        # Expecting obj_type
        obj_type = request.query_params.get('obj_type')
        user_id = request.headers.get('UserId')

        # If no user id, should return inform frontend & return empty list
        if not user_id:
            return Response(responsedata(False,"User Id not provided",[]),status=400)
        
        # define filter query. This is done so that in future if we  want to add 
        # dynamic filter attributes, can be easily achieved in same way...
        filter_query = dict(user_id=user_id)
        if obj_type:
            filter_query["obj_type"]=obj_type
        
        # filtering favourites for user and returning serialized data
        favs = Favourites.objects.filter(**filter_query)
        favourite_data = FavouritesSerializer(favs,many=True).data
        try:
            message = f"{obj_type.upper()} Favourites list"
        except:
            message = "Favourites list"
        return Response(responsedata(True,message,favourite_data),status=status.HTTP_200_OK)

    def post(self,request,pk=None):
        # No auth added, expecting user Id from headers
        user_id = request.headers.get('UserId')
        data = request.data
        data['user'] = user_id
        
        # Fetching favourites
        if Favourites.objects.filter(user_id=user_id,obj_type=data.get("obj_type"),name=data.get('name')).exists():
            return Response(responsedata(False,"Already added to favourites"),status=406)
        
        # validation and saving data
        fav_serializer = FavouritesSerializer(data=data)
        try:
            if fav_serializer.is_valid(raise_exception=True):
                fav_serializer.save()
                return Response(responsedata(False,"Successfully added to favourites"),status=201)
        except Exception as e:
            return Response(responsedata(False,str(e)),status=400)

    def put(self,request,pk):
        user_id = request.headers.get('UserId')
        # If no user id, should return inform frontend & return empty list
        if not user_id:
            return Response(responsedata(False,"User Id not provided",[]),status=400)
        if not pk:
            return Response(responsedata(False,"Invalid favourite id, Favourite not found",[]),status=404)
        
        data = request.data
        if Favourites.objects.filter(user_id=user_id,id=pk).exists():
            fav = Favourites.objects.filter(user_id=user_id,id=pk).first()
            fav_serializer = FavouritesSerializer(fav,data=data,partial=True)
            if fav_serializer.is_valid():
                fav_serializer.save()
                return Response(responsedata(True,"Favourite Updated",fav_serializer.data),status=200)
            else:
                return Response(responsedata(False,str(fav_serializer.errors)),status=400)
        else:
            return Response(responsedata(False,"Favourite not found"),status=404)

    def delete(self,request,pk):
        user_id = request.headers.get('UserId')
        # If no user id, should return inform frontend & return empty list
        if not user_id:
            return Response(responsedata(False,"User Id not provided",[]),status=400)
        if not pk:
            return Response(responsedata(False,"Invalid favourite id, Favourite not found",[]),status=404)
        if Favourites.objects.filter(user_id=user_id,id=pk).exists():
            Favourites.objects.filter(user_id=user_id,id=pk).first().delete()
            return Response(responsedata(True,"Favourite Removed"),status=204)
        else:
            return Response(responsedata(False,"Favourite not found"),status=404)