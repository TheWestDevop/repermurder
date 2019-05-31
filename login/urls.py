from django.urls import path
from .views import *

urlpatterns = [
    path('',login,name="login"),
    path('gen',gen,name="gen")
]