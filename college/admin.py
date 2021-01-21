from django.contrib import admin
from .models import Colleges
from .models import User
from .models import Categories
from .models import FoodItems
from .models import Order
from .models import OrderDetails
from .models import Favourites


admin.site.register(Colleges)
admin.site.register(Categories)
admin.site.register(FoodItems)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Favourites)

