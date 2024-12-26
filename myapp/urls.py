from django.urls import path

from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path("file/<str:file_hash>/", views.get_file, name='get-file'),
]
