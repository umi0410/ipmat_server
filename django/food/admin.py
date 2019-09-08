from django.contrib import admin
from .models import *

# Register your models here.
class FoodAdmin(admin.ModelAdmin):
    list_display = ["__str__", "img", "oneline_desc", "creator"]

class FoodBookAdmin(admin.ModelAdmin):
    def getLength(self, foodBook):
        return str(len(foodBook.food.all()))+" 개"
    getLength.short_description="음식 개수"

    list_display=["__str__", "food_book_name", "getLength"]
admin.site.register(Food,FoodAdmin)
# admin.site.register(FoodComment)
admin.site.register(FoodBook, FoodBookAdmin)

class FoodCategoryAdmin(admin.ModelAdmin):
    def getLength(self, category):
        return len(category.food_set.all())
        # return 10
    getLength.admin_order_field="pk"
    getLength.short_description="Length of Food"

    list_display = ["__str__", "categoryName",  "getLength"]
def getAnswerFoodName(f, participant_row):
    return participant_row.question.answer.food_name

admin.site.register(FoodSubCategory, FoodCategoryAdmin)