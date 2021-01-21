from rest_framework import serializers

from .models import Colleges, \
    User, \
    Categories, \
    FoodItems


class FoodItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = ("id", "name", "price", "short_des", "college", "category")


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("id", "name", "short_desc", "college")


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colleges
        fields = ("id", "name_college", "email", "phone", "address", "city")


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ("id", "user_name", "email", "phone", "password", "password2", "college")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            user_name=self.validated_data['user_name'],
            phone=self.validated_data['phone'],
            college=self.validated_data['college'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Passwords don't match."})
        user.set_password(password)
        user.save()
        return user
