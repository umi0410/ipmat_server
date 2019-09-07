from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
import json
from .models import *
from member.models import Member
from food.models import Food
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import time, hashlib
# Create your views here.

def getExamFromParticipant(participantId):
    participatedExams=[]
    for exam in FoodTest.objects.all():
        if exam.participantanswer_set.filter(member_id=participantId).exists():
            participatedExams.append(exam)
    return participatedExams
def getParicipantsFromExam(examId):
    participantAnswers=[]
    participants=[]
    if FoodTest.objects.filter(id=examId).exists:
        participantAnswers=FoodTest.objects.get(id=examId).participantanswer_set.all()
    for guesses in participantAnswers:
        if not guesses.member_id in participants:
            participants.append(guesses.member_id)
    return participants

def readQuestion(request):
    # TestRows.objects.first().row1.left_food
    # 첫번쨰 테스트 로우만 가져옴
    questions=TestRowOne.objects.all().order_by("?")
    data=[]
    index=0
    for question in questions:
        _q={
            "question_id" : question.id,
            "question_index" : index,
            "left_food" : {
                "id":question.left_food.id,
                "food_name":question.left_food.food_name},
            "right_food":{
                "id":question.right_food.id,
                "food_name":question.right_food.food_name}
        }
        data.append(_q)
        index += 1

    # rows_json = serializers.serialize('json', rows)
    # return HttpResponse(rows_json, content_type='application/json')
    return HttpResponse(json.dumps(data))

@csrf_exempt
def readMyExamList(request):
    if request.method == "POST":
        #print(request.POST)
        # m=Member.objects.get(_id=request.POST["id"])
        
        data=[]
        for test in FoodTest.objects.filter(author=request.POST["id"]):
            _d={
                "type":"author",
                "author":test.author._id,
                "exam_id":test.id,
                "title":test.title,
                "hashId":test.hashId,
                "numOfParticipants":len(getParicipantsFromExam(test.id))
            }
            data.append(_d)
        participatedExams=getExamFromParticipant(request.POST["id"])
        # for test in FoodTest.objects.filter(participant=request.POST["id"]):
        for test in participatedExams:
            _d={
                "type":"participant",
                "author":test.author._id,
                "exam_id":test.id,
                "title":test.title,
                "hashId":test.hashId,
                "numOfParticipants":len(getParicipantsFromExam(test.id))
            }
            data.append(_d)
        print(data)
        return HttpResponse(json.dumps(data))

def readExamDetail(request):
    #print(request.GET)
    if "hashId" in request.GET:
        exam = FoodTest.objects.get(hashId=request.GET["hashId"])
    else:
        exam = FoodTest.objects.get(id=request.GET["examId"])


    data={"examId":exam.pk, "title":exam.title, "author":exam.author.pk, "questions":[]}
    cnt=0
    for question in exam.testrows_set.all():
        #print(question)
        data["questions"].append({
            "question_index":cnt,
            "question_id": question.id,
            "left_food":{
                "id" : question.row.left_food.id,
                "food_name" : question.row.left_food.food_name
            } ,
            "right_food":{
                "id":question.row.right_food.id,
                "food_name" : question.row.right_food.food_name,
            }
        })
        cnt+=1

    print( json.dumps(data))

    return HttpResponse(json.dumps(data))

@csrf_exempt
def createAnswer(request):
    if request.method == "POST":
        # print(request.POST)
        data=json.loads(request.POST["data"])
        print(data)
        if data["examId"]:
            examObj=FoodTest.objects.get(id=data["examId"])
        else: # hashId로 풀어제끼는 경우
            examObj=FoodTest.objects.get(hashId=data["examHashId"])

        print(data["examHashId"])
        try:
            _exAnswers= ParticipantAnswer.objects.filter(member=data["participant"], test=examObj)
            if (len(_exAnswers) != 0 ) : 
                _exAnswers.delete()
                # print("풀었던 문제라 원래 답 삭제됨")
            for question in data["questions"]:
                answer=ParticipantAnswer(
                    member=Member.objects.get(pk=data["participant"]),
                    question=TestRows.objects.get(id=question["question_id"]),
                    answer=Food.objects.get(id=question["answer_food_id"]),
                    test=examObj
                )
                answer.save()
            answer.question.test.participant.add(Member.objects.get(pk=data["participant"]))
                
        except Exception as e:
            # print("=======")
            # print(_exAnswer)
            # print("=======")
            print (e)
        return HttpResponse("good")
    
def read(request, id):
    testData=FoodTest.objects.get(id=id)
    usedRows=testData.testrows_set.all() # queryset 임.
    # scores=testData.score_set.first()
    data={}
    data["testId"]=id
    data["title"]=testData.title
    # data["scores"]=scores.name
    data["questions"]=[]

    for row in usedRows:
        data["questions"].append(row.id)

    return HttpResponse(json.dumps(data))

@csrf_exempt
def create(request):
    if request.method == "POST":
        print(request.POST["data"])
        data=json.loads(request.POST["data"])
        author=Member.objects.get(_id=data["author"])

        # hash id 작업
        h=hashlib.sha1()
        h.update(str(time.time()).encode())
        hashId=h.hexdigest()[:5]

        while len(FoodTest.objects.filter(hashId=hashId)) != 0:
            h.update(str(time.time()).encode())
            hashId=h.hexdigest()[:5]

        newFoodTest=FoodTest(title=data["title"], author=author, hashId=hashId)
        newFoodTest.save()
        print(hashId)
        for qna in data["questions"]:
            questionRow=TestRows(test=newFoodTest, member=author,
                row=TestRowOne.objects.get(id=qna["question_id"]),
                answer=Food.objects.get(id=qna["answer_food_id"])
            )
            questionRow.save()
            print(questionRow)
        
        print("end")
        return HttpResponse("good")

@csrf_exempt
def readResultAll(request):
    # if request.method == "POST":
        # print(request.POST)
        # exam =FoodTest.objects.get(id=request.POST["examId"])
        exam =FoodTest.objects.get(id=request.GET["examId"])
        data={
            "examId":exam.id,
            "title":exam.title,
            "questions":[],
            "participants":{}
        }
        #questionRow에는 row_set()이 있고 그 안에는 푸드들이 있고 answer, participant_answer이 있다.
        for questionRow in TestRows.objects.select_related().filter(test_id=exam.id):
            _d={}
            _d["left_food"]={
                "food_id":questionRow.row.left_food.id,
                "food_name":questionRow.row.left_food.food_name
            }
            _d["right_food"]={
                "food_id":questionRow.row.right_food.id,
                "food_name":questionRow.row.right_food.food_name
            }
            _d["answer_food"]={
                "food_id":questionRow.answer.id,
                "food_name":questionRow.answer.food_name
            }
            data["questions"].append(_d)

            
            for guess in ParticipantAnswer.objects.select_related().filter(question=questionRow.id):
                # 이 멤버의 정답제출이 없었다면 빈 리스트로 우선 등록
                
                print(guess)
                if guess.member.pk in data["participants"]:
                    data["participants"][guess.member._id]["answers"].append(guess.answer.id)
                else:
                    data["participants"][guess.member._id]={
                        "answers":[guess.answer.id]
                    }
        
        print(json.dumps(data))

        for memberPk in data["participants"].keys():
            score = 0
            for index in range(len(data["questions"])):
                if data["questions"][index]["answer_food"]["food_id"] == data["participants"][memberPk]["answers"][index]:
                    score+=1
            data["participants"][memberPk]["score"]=score
            
        return HttpResponse(json.dumps(data))

def readScoreOfParticiapnts(request, examId):
    exam = FoodTest.objects.get(id=examId)
    data={
        "examId":exam.id,
        "title":exam.title,
        "numOfQuestions":0,
        "participants":[]
    }
    if( len(getParicipantsFromExam(exam.id)) == 0):
        return HttpResponse(json.dumps(data))
    #questionRow에는 row_set()이 있고 그 안에는 푸드들이 있고 answer, participant_answer이 있다.
    else:
        # question id들의 순서에 따라 정답, 추측들을 담아
        questionIds=[]
        answerFoodIds=[]
        scores=[]
        #우선 question id를 담고 동시에 그 question id에 대한 정답도 담아
        for row in TestRows.objects.filter(test=exam):
            questionIds.append(row.pk) 
            answerFoodIds.append(row.answer.pk)
        data["numOfQuestions"]=len(questionIds)

        # 이제는 exam id에 따른 participant들의 추측들을 담고 점수를 메길 것임.
        for participant in getParicipantsFromExam(exam.id):
            guesses=[]
            for questionId in questionIds:
                print("멤버아이디 : ", participant)
                print("question : ", questionId)
                guesses.append(ParticipantAnswer.objects.get(member_id=participant, question_id=questionId).answer.id)
            score=0
            for i in range(len(questionIds)):
                if answerFoodIds[i] == guesses[i]:
                    print(answerFoodIds[i], guesses[i], "정답")
                    score+=1
                else:
                    print(answerFoodIds[i], guesses[i], "오답")
            # sort by ( score, participant id)
            scores.append( (score, participant) )
        scores.sort(reverse=True)
        for i in range(len(scores)):
            data["participants"].append({"memberId" : scores[i][1]})
            data["participants"][-1]["score"]=scores[i][0]
            data["participants"][-1]["rank"]=i+1
    print(json.dumps(data))
    return HttpResponse(json.dumps(data))

@csrf_exempt
def readResult(request):
    if request.method == "POST":
        print(request.POST)
        # exam =FoodTest.objects.get(id=request.POST["examId"])
        exam = FoodTest.objects.get(id=request.POST["examId"])
        memberId = request.POST["memberId"]
        data={
            "examId":exam.id,
            "title":exam.title,
            "questions":[],
            "participants":{}
        }
        if( len(getParicipantsFromExam(exam.id)) == 0):
            return HttpResponseBadRequest("No Answer")
        #questionRow에는 row_set()이 있고 그 안에는 푸드들이 있고 answer, participant_answer이 있다.
        for questionRow in TestRows.objects.select_related().filter(test_id=exam.id):
            _d={}
            _d["left_food"]={
                "id":questionRow.row.left_food.id,
                "food_name":questionRow.row.left_food.food_name
            }
            _d["right_food"]={
                "id":questionRow.row.right_food.id,
                "food_name":questionRow.row.right_food.food_name
            }
            _d["answer_food"]={
                "id":questionRow.answer.id,
                "food_name":questionRow.answer.food_name
            }
            data["questions"].append(_d)

            
            for guess in ParticipantAnswer.objects.select_related().filter(question=questionRow.id):
                # 이 멤버의 정답제출이 없었다면 빈 리스트로 우선 등록
                # print("----")   
                # print(guess)
                if guess.member.pk in data["participants"]:
                    data["participants"][guess.member._id]["answers"].append(guess.answer.id)
                else:
                    data["participants"][guess.member._id]={
                        "answers":[guess.answer.id]
                    }
        
        # print(json.dumps(data))

        for memberPk in data["participants"].keys():
            score = 0
            for index in range(len(data["questions"])):
                if data["questions"][index]["answer_food"]["id"] == data["participants"][memberPk]["answers"][index]:
                    score+=1
            data["participants"][memberPk]["score"]=score
        # print(data)
        return HttpResponse(json.dumps(data))

@csrf_exempt
def readParticipants(request):
    if request.method == "POST":
        print(request.POST)
        participants=getParicipantsFromExam(request.POST["examId"])
        data={"participants":participants}
        print(data)
        return HttpResponse(json.dumps(data))

@csrf_exempt
def isExistFromHashId(request):
    if request.method=="POST":
        if len(FoodTest.objects.filter(hashId=request.POST["hashId"])) != 0:
            return HttpResponse("exist")
        else : return HttpResponseBadRequest("Not exist")

def deleteExam(request):
    print(request.GET)
    authorId=request.GET["authorId"]
    examId=request.GET["examId"]
    querySet=FoodTest.objects.filter(id = examId, author_id=authorId)
    if querySet.exists():
        print("deleting..")
        print(querySet.first())
        querySet.first().delete()

        return HttpResponse("deleted")
    else:
        return HttpResponseBadRequest("not deleted")

def deleteParticipant(request):
    #필요한 것은 계정의 session과 시험지의 id

    print(request.GET)
    try:
        member=Member.objects.get(session_key=request.GET["sessionKey"])
        if ParticipantAnswer.objects.filter(member=member, test_id=request.GET["examId"]).exists():
            pa=ParticipantAnswer.objects.filter(member=member, test_id=request.GET["examId"])
            print("deleted")
            pa.delete()
    except ObjectDoesNotExist:
        return HttpResponseBadRequest(".")
    return HttpResponse("deleted!")