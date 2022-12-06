from .models import Favourites

def responsedata(status, message, data=None):
    # Function for creating standard response format
    if status: # success case
        return {"status": status, "message": message, "data": data}
    else:
        return {"status": status, "message": message}


def get_query_name(query,obj_type):
    """
    get_query_name : function for getting actual name if custom name from favourite data 
    is passed in params for querying
    """
    if Favourites.objects.filter(custom_name=query,obj_type=obj_type).exists():
        return Favourites.objects.filter(custom_name=query,obj_type=obj_type).first().name
    else:
        return query

def get_is_favourite(name,obj_type,user_id):
    # function for returning favourite name and is_favourite value
    if not user_id:
        return False,name
    elif Favourites.objects.filter(user_id=user_id,name=name,obj_type=obj_type).exists():
        fav = Favourites.objects.filter(user_id=user_id,name=name,obj_type=obj_type).first()
        if fav.custom_name:
            name = fav.custom_name
        return True,name
    else:
        return False,name


def get_formatted_data(obj_type,results,user_id):
    """
    function for returns desired keys from response and checking is_favourite
    """
    result = []
    try:
        for i in results:
            # keys are different for planets and movies so different mapping used
            if obj_type=='Planets':
                is_favourite,name = get_is_favourite(i['name'],obj_type=obj_type,user_id=user_id)
                result.append({"name":name,"created":i['created'],"updated":i["edited"],"url":i["url"],"is_favourite":is_favourite})
            else:
                is_favourite,name = get_is_favourite(i['title'],obj_type=obj_type,user_id=user_id)
                result.append({"title":name,"release_date":i['release_date'],"created":i['created'],"updated":i['edited'],"is_favourite":is_favourite})
    except Exception as e:
        print(str(e))
    return result