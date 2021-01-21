from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from college.serializers import FoodItemsSerializer, CollegeSerializer, CategoriesSerializer
from college.models import FoodItems, Categories, Colleges
from rest_framework.decorators import api_view


@api_view(['POST'])
def register_college(request):
    serializer = CollegeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# just for testing purpose
def get_college(request):
    colleges_list = CollegeSerializer(
        Colleges.objects.all().order_by("-id"),
        many=True,
        context={"request": request}
    ).data
    return JsonResponse({"colleges": colleges_list})


def college_get_meals(request, college_id):
    all_meals = FoodItemsSerializer(
        FoodItems.objects.filter(college_id=college_id).order_by("-category_id"),
        many=True,
        context={"request": request}
    ).data
    return JsonResponse({"all_meals": all_meals})


# check for category id

@api_view(['POST'])
def college_add_meal(request, college_id, category_id):
    if request.method == "POST":
        add_meal = FoodItemsSerializer(data=request.data)
        if add_meal.is_valid():
            add_meal.save()
            return Response(add_meal.data, status=status.HTTP_201_CREATED)
        return Response(add_meal.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def meal_detail(request, college_id, category_id, meal_id):
    try:
        snippet = FoodItems.objects.get(college_id=college_id, category_id=category_id, pk=meal_id)
    except FoodItems.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = FoodItemsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def college_add_category(request, college_id):
    serializer = CategoriesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# wrong method of college id we will get it from auth


@api_view(['PUT', 'DELETE'])
def category_detail(request, college_id, category_id):
    try:
        snippet = Categories.objects.get(college_id=college_id, category_id=category_id)
    except Categories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CategoriesSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
