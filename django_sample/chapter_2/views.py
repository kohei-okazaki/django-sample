from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import RegistForm

# Create your views here.
"""
Created on 2020/05/06
# 画面毎にviewを用意、同機能の画面で扱うFormは1つform.pyで定義
@author: okazaki
@version: 1.0.0
"""

view_name = {
        "index_view_name": "Index画面",
        "input_view_name": "入力画面",
        "confirm_view_name": "登録情報入力確認画面",
        "complete_view_name": "登録完了画面",
    }

"""
Index画面のView
"""
class IndexView(TemplateView):

    def __init__(self):
        self.param = {
                "title": view_name["index_view_name"],
                "index_view_name": view_name["index_view_name"],
                "input_view_name": view_name["input_view_name"],
            }

    def get(self, request):
        return render(request, "chapter_2/index.html", self.param)

    def post(self, request):
        return self.get(self, request)

"""
入力画面のView
"""
class InputView(TemplateView):

    def __init__(self):
        self.param = {
                "title": view_name["input_view_name"],
            }

    def get(self, request):
        return render(request, "chapter_2/input.html", self.param)

"""
登録情報入力確認画面のView
"""
class ConfirmView(TemplateView):

    def __init__(self):
        self.param = {
                "title": view_name["confirm_view_name"]
            }

    def post(self, request):
        self.param["id"] = request.POST["id"]
        self.param["password"] = request.POST["password"]
        self.param["confirm_password"] = request.POST["confirm_password"]
        return render(request, "chapter_2/confirm.html", self.param)

"""
登録完了画面のView
"""
class CompleteView(TemplateView):

    def __init__(self):
        self.param = {
                "title": view_name["complete_view_name"],
                "index_view_name": view_name["index_view_name"],
            }

    def post(self, request):

        return render(request, "chapter_2/complete.html", self.param)
