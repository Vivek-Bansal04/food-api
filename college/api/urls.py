from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_college, name='register_college'),
    path('get_college', views.get_college, name='get_college'),
    path('<college_id>/category/add/', views.college_add_category, name='college_add_category'),
    path('<college_id>/<category_id>/category', views.category_detail, name="category_detail"),
    path('<college_id>/meals/', views.college_get_meals, name='college_get_meals'),
    path('<college_id>/<category_id>/meal/add/', views.college_add_meal, name='college-add-meal'),
    path('<college_id>/<category_id>/<meal_id>/meal', views.meal_detail, name='meal_detail')
]
