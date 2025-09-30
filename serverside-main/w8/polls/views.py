from django.shortcuts import render, redirect
from django.views import View

from .models import Question, Choice


class IndexView(View):
    def get(self, request):
        question_list = Question.objects.order_by("-pub_date")
        context = {"question_list": question_list}
        return render(request, "index.html", context)

class PollView(View):

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        return render(request, "detail.html", {
            "question": question,
            "choices": question.choice_set.all()
        })

class VoteView(View):

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        return render(request, "vote.html", {
            "question": question,
            "choices": question.choice_set.all()
        })
    
    def post(self, request, question_id):
        choice_id = request.POST.get('choice')
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()
        return redirect("detail", question_id=question_id)