from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new-meating', views.new_meating, name='new_meating'),
    path('<int:meating_id>/', views.meating, name='meating'),
    path('<int:meating_id>/submit', views.submit_meating, name='submit_meating'),
]

