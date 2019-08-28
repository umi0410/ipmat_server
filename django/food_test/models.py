from django.db import models
from food.models import FoodBook, Food
from member.models import Member
# Create your models here.
def imgUpload(instance, _name):
    return "imgs/"+_name


class TestRowOne(models.Model):
    
    left_food=models.ForeignKey(Food, on_delete=models.CASCADE, related_name="left")
    right_food=models.ForeignKey(Food, on_delete=models.CASCADE, related_name="right")
    
    def __str__(self):
        return self.left_food.food_name+" vs "+self.right_food.food_name

class FoodTest(models.Model):
    title=models.CharField(max_length=30)
    author=models.ForeignKey(Member, on_delete=models.CASCADE)
    hashId=models.CharField(max_length=5)
    def __str__(self):
        return str(self.id)+". Test["+self.author._id+"] "+self.title

# 이렇게 simple 하게 담고 Test에서 자신을 Foreign Key로 갖는 애들을 뽑아
class TestRows(models.Model):
    test=models.ForeignKey(FoodTest,  on_delete=models.CASCADE)
    member=models.ForeignKey(Member, on_delete=models.CASCADE)
    row=models.ForeignKey(TestRowOne, on_delete=models.CASCADE)
    answer=models.ForeignKey(Food, on_delete = models.CASCADE)
class ParticipantAnswer(models.Model):
    member=models.ForeignKey(Member, on_delete=models.CASCADE)
    question=models.ForeignKey(TestRows, on_delete=models.CASCADE)
    answer=models.ForeignKey(Food, on_delete = models.CASCADE)
    test=models.ForeignKey(FoodTest,  on_delete=models.CASCADE)

    def __str__(self):
        return "ParticipantAnswer<"+str(self.id)+"> "+self.member.pk+" "+str(self.question.id)+"th answer in "+self.question.test.title[:5]
    
class Score(models.Model):
    test=models.ForeignKey(FoodTest,  on_delete=models.CASCADE)
    participant=models.ForeignKey(Member, on_delete=models.CASCADE)
    score=models.IntegerField()

