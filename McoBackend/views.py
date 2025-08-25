from django.http import JsonResponse
from django.conf import settings

def get_users(request):
    users_collection = settings.MONGO_DB["users"]
    users = list(users_collection.find({}, {"_id": 0}))
    return JsonResponse(users, safe=False)
