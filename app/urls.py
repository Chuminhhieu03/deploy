from django.urls import path
from app import views
from app.views import GetData

urlpatterns = [
    path('', views.index, name='index'),
    path('get_data', GetData.as_view(), name='get_data'),
]



