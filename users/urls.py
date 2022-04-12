
from django.urls import path
from users import views

urlpatterns = [
    path('registation/',views.registation),
    path('login/', views.login_user),
    #path('logout/')
]