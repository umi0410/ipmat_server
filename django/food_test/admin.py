from django.contrib import admin
from .models import *

from .models import  *
class TestRowOneAdmin   (admin.ModelAdmin):
        
    list_display = ["__str__", 'left_food', 'right_food'] # 커스터마이징 코드
    search_fields=['id',"left_food__food_name", "right_food__food_name"] # 커스터마이징 코드

class ParticipantAnswerAdmin(admin.ModelAdmin):

    def getLeftFoodName(self, participant_row):
        return participant_row.question.row.left_food.food_name
    def getRightFoodName(f, participant_row):
        return participant_row.question.row.right_food.food_name
    def getAnswerFoodName(f, participant_row):
        return participant_row.question.answer.food_name

    # Not sure how to order..
    getLeftFoodName.admin_order_field  = 'pk'  #Allows column order sorting
    getLeftFoodName.short_description = 'Left Food'  #Renames column head

    getRightFoodName.admin_order_field  = 'pk'  #Allows column order sorting
    getRightFoodName.short_description = 'Right Food'  #Renames column head

    getAnswerFoodName.admin_order_field  = 'pk'  #Allows column order sorting
    getAnswerFoodName.short_description = 'Answer Food'  #Renames column head

    list_display=["__str__", "getLeftFoodName", "getRightFoodName", "getAnswerFoodName"]


# Register your models here.
admin.site.register(TestRowOne, TestRowOneAdmin)
admin.site.register(FoodTest)
admin.site.register(TestRows)
admin.site.register(ParticipantAnswer, ParticipantAnswerAdmin)
# admin.site.register(Score)

# admin.site.register(FoodQuestion)
# admin.site.register(FoodTestRaw)
# admin.site.register(Score)
