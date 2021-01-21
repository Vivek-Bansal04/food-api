from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.utils import timezone
import json


from .models import Categories, FoodItems, User, Colleges, Order, OrderDetails
from .serializers import CategoriesSerializer, FoodItemsSerializer, UserSerializer


# Create your views here.


def get_categories(request, college_id):
    categories = CategoriesSerializer(
        Categories.objects.filter(college_id=college_id).order_by("-name"),
        many=True,
        context={"request": request}
    ).data
    return JsonResponse({"categories": categories})


def get_meals(request, college_id, category_id):
    meals = FoodItemsSerializer(
        FoodItems.objects.filter(college_id=college_id, category_id=category_id).order_by("-name"),
        many=True,
        context={"request": request}
    ).data
    return JsonResponse({"meals": meals})


def search(request, college_id):
    if request.method == 'GET':
        search_meal = request.GET.get('search')
        searched_item = FoodItems.objects.filter(college_id=college_id)
        search_item = searched_item.filter(name__icontains=search_meal)
        meal = FoodItemsSerializer(search_item, many=True, context={"request": request}).data
        return JsonResponse({"meal": meal})
    # else


def add_order(request):
    if request.method == "POST":
        order_details = json.loads(request.POST["order_details"])
        # get details

        order_total = 0
        for meal in order_details:
            order_total += FoodItems.objects.get(id=meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:
            # Step 1 - Create an Order
            order = Order.objects.create(
                # check for error in user
                # could use request.POST["user_id"]
                user=User.objects.get(id=request.POST["user_id"]),
                college_id=request.POST["college_id"],
                total=order_total,
                # status=Order.COOKING,
            )

            # Step 2 - Create Order details
            for meal in order_details:
                OrderDetails.objects.create(
                    order=order,
                    meal_id=meal["meal_id"],
                    quantity=meal["quantity"],
                    sub_total=FoodItems.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                )

            return JsonResponse({"status": "success"})


# else condition left

@api_view(['POST', ])
def signup_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            users = serializer.save()
            data['response'] = "successfully registered ."
            data['email'] = users.email
            data['user_name'] = users.user_name
            data['phone'] = users.phone
            #token = Token.objects.get(user=users).key
            #data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
