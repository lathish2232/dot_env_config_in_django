#from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from users.user_impl import user_registation,user_login

# Create your views here.


@csrf_exempt
@api_view(['POST'])
def registation(request):
        return user_registation(request)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
        return user_login(request)