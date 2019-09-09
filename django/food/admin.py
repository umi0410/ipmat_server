from django.contrib import admin
from .models import *

# Register your models here.
STR_KHU_RESTAURANT="경희대맛집"

class FoodAdmin(admin.ModelAdmin):
    def addKHURestaurant(self, request, queryset):
        for query in queryset:
            query.category.add(FoodSubCategory.objects.get(categoryName=STR_KHU_RESTAURANT))
    addKHURestaurant.short_description = "add the category named "+STR_KHU_RESTAURANT
    def removeKHURestaurant(self, request, queryset):
        for query in queryset:
            query.category.add(FoodSubCategory.objects.get(categoryName=STR_KHU_RESTAURANT))
    removeKHURestaurant.short_description = "remove the category named " + STR_KHU_RESTAURANT

    list_display = ["__str__", "img", "oneline_desc", "creator"]
    actions=[addKHURestaurant, removeKHURestaurant]

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