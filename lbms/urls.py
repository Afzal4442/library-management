from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('create', views.create, name='create'),
    path('view/<str:id>', views.view, name='view'),
    path('edit/<str:id>', views.edit, name='edit'),
    path('delete', views.delete, name='delete'),
]