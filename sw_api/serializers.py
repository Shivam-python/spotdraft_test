import requests
from rest_framework import serializers
from .models import *
from .utils import get_formatted_data
from spotdraft_test.settings import  MOVIES_URL,PLANETS_URL

class FavouritesSerializer(serializers.ModelSerializer):
    """
    Model Serializer for validation.
    """
    obj_type=serializers.CharField(required=True)
    class Meta:
        model = Favourites
        fields = '__all__'

    def validate_obj_type(self, obj_type):
        # changing obj type to capitalized value
        # since field is required no need to add Validation error exception code
        # custom exception can be raised like :
        obj_type = obj_type.capitalize()
        if not obj_type in ['Planets','Movies']:
            raise serializers.ValidationError("Invalid object type")
        return obj_type

    def to_representation(self, instance):
        # Overriding the default data and adding data from SWAPI.dev
        response = super().to_representation(instance)
        try:
            # fetching URL dynamically
            url = globals()[f"{instance.obj_type.upper()}_URL"]
            # adding search query
            url+=f'?search={instance.name}'
            api_response = requests.get(url)
            api_response = api_response.json()

            # using formatter function to get desired key-values from api-response
            # and updating serialized response.
            response_data= get_formatted_data(obj_type=instance.obj_type,results=api_response['results'],user_id=instance.user.id)
            response_data = response_data[0]

            # removing modified name value. returning original name of favourite obj
            response_data.pop('name')
            response.update(**response_data)
        except Exception as e:
            print(str(e))
        return response
