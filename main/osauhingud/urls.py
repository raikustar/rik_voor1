from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name="home"),
    path('details/<int:osauhing_id>/', views.view_company, name="view_company"),
    path('add/', views.add_company, name="add_new"),
]