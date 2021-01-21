from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup', views.signup_view, name="signup"),
    path('login', obtain_auth_token, name="login"),
    path('<college_id>/categories', views.get_categories, name='home'),
    path('<college_id>/meals/<category_id>', views.get_meals, name='meals'),
    path('<college_id>/search/', views.search, name='search'),
    path('<college_id>/order/add', views.add_order)

]