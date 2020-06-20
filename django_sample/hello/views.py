# -*- coding: utf-8 -*-
from django.db.models.aggregates import Count, Avg, Min, Max
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from hello.forms import HelloForm, HelloSearchForm, HelloInsertForm, HelloModelMapper, HelloFindForm, ValidForm, \
    MessageForm
from hello.models import Friend, Message
from django.core.paginator import Paginator

# Create your views here.

# 1
# def index(request):
#     if "msg" in request.GET:
#         msg = request.GET["msg"]
#         result = "Hello Django!!!<br>you typed '" + msg + "'."
#     else:
#         result = "msgパラメータが未設定です"
#     return HttpResponse(result)

# 2
# def index(request, id, nickname):
#     result = "あなたのIDは" + str(id) + ", 名前は" + nickname
#     return HttpResponse(result)

# 3
# def index(request):
#     if "msg" in request.GET:
#         msg = request.GET["msg"]
#     else:
#         msg = "msgパラメータが未設定です"

#     param = {
#             "title": "Hello/Index",
#             "msg": msg,
#         }
#     return render(request, "hello/index.html", param)

# 4
# def index(request):
#     param = {
#             "title": "Hello/Index",
#             "msg": "Indexのページです",
#             "goto": "next",
#         }
#     return render(request, "hello/index.html", param)

# def next(request):
#     param = {
#             "title": "Hello/Next",
#             "msg": "Nextのページです",
#             "goto": "index",
#         }
#     return render(request, "hello/index.html", param)

# 5
# def index(request):
#     param = {
#             "title": "Hello/Index",
#             "msg": "あなたの名前は？",
#         }
#     return render(request, "hello/index.html", param)

# def form(request):
#     msg = request.POST["msg"]
#     param = {
#             "title": "Hello/Form",
#             "msg": msg,
#         }
#     return render(request, "hello/index.html", param)

# 6
# def index(request):
#     param = {
#             "title": "Hello/Index",
#             "msg": "あなたの情報:",
#             "form": HelloForm()
#         }

#     if (request.method == "POST"):
#         param["msg"] = "名前=" + request.POST["name"] + \
#             "<br>メール=" + request.POST["mail"] + \
#             "<br>年齢=" + request.POST["age"]
#         param["form"] = HelloForm(request.POST)

#     return render(request, "hello/index.html", param)


# 7
class HelloView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "Index画面",
            "msg": "あなたの情報:",
            "form": HelloForm()
        }

    # GET通信の場合
    def get(self, request):
        return render(request, "hello/index.html", self.param)

    # POST通信の場合
    def post(self, request):
        if ("check" in request.POST):
            strBoolResult = "チェックあり"
        else:
            strBoolResult = "チェックなし"

        msg = "名前=" + request.POST["name"] + \
            "<br>メール=" + request.POST["mail"] + \
            "<br>年齢=" + request.POST["age"] + \
            "<br>誕生日=" + request.POST["birthday"] + \
            "<br>チェック有無=" + strBoolResult + \
            "<br>3択チェック有無=" + request.POST["check_other"] + \
            "<br>プルダウン=" + request.POST["pulldown"] + \
            "<br>ラジオボタン=" + request.POST["radio_button"] + \
            "<br>セレクトリスト=" + request.POST["select_list"] + \
            "<br>多数セレクトリスト=" + str(request.POST.getlist("multi_select_list"))

        self.param["msg"] = msg
        self.param["form"] = HelloForm(request.POST)
        return render(request, "hello/index.html", self.param)

# def __new_str__(self):
#     result = ""
#     for item in self:
#         result += "<tr>"
#         for k in item:
#             result += "<td>" + str(k) + "=" + str(item[k]) + "</td>"
#         result += "</tr>"
#     return result
# QuerySet.__str__ = __new_str__


class HelloListView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "ID検索画面",
            "form": HelloSearchForm(),
            "entity_list":[],
        }

    # GET通信の場合
    def get(self, request, page=1):

        # 全カラムをQuerySetのリストでselect
        # self.param["entity_list"] = Friend.objects.all()
        # 全カラムをmapとしてselect
        # self.param["entity_list"] = Friend.objects.all().values()
        # IDとNameのみselect
        # self.param["entity_list"] = Friend.objects.all().values("id", "name")
        # IDとNameとAgeのみをListとしてselect
        # self.param["entity_list"] = Friend.objects.all().values_list("id", "name", "age")
        # レコードの先頭を取得
        # self.param["entity_list"] = [Friend.objects.all().values().first()]
        # レコードの最後を取得
        # self.param["entity_list"] = [Friend.objects.all().values().last()]
        # レコードのカウントを取得
        # self.param["cnt"] = Friend.objects.all().values().count()

        # 全件取得。ただし、ユーザ名で並べ替え
        # self.param["entity_list"] = Friend.objects.all().order_by("age", "mail")
        # 全件取得。ただし、ユーザ名で並べ替え かつ先頭5件を取得
        # self.param["entity_list"] = Friend.objects.all().order_by("age", "mail")[0:5]

        sql = "select * from hello_friend"
        print("SQL--->" + sql)
        entity_list = Friend.objects.raw(sql)

        paginator = Paginator(entity_list, 5)
        self.param["entity_list"] = paginator.get_page(page)

        self.param["record_count"] = Friend.objects.aggregate(Count("age"))["age__count"]
        self.param["age_average"] = Friend.objects.aggregate(Avg("age"))["age__avg"]
        self.param["age_min"] = Friend.objects.aggregate(Min("age"))["age__min"]
        self.param["age_max"] = Friend.objects.aggregate(Max("age"))["age__max"]
        return render(request, "hello/search.html", self.param)

    # POST通信の場合
    def post(self, request):

        entity_id = request.POST["id"]
        # IDで検索
        entity = Friend.objects.get(id=entity_id)
        self.param["entity_list"] = [entity]
        self.param["form"] = HelloSearchForm(request.POST)
        return render(request, "hello/search.html", self.param)


class HelloInsertView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "作成画面",
            "form": HelloModelMapper()
        }

    # GET通信の場合
    def get(self, request):
        return render(request, "hello/insert.html", self.param)

    # POSTの場合
    def post(self, request):

        # 画面からの入力値を個別で入れる場合
        # entity = Friend(name=request.POST["name"], mail=request.POST["mail"], age=request.POST["age"],\
        #        gender="gender" in request.POST, birthday=request.POST["birthday"])

        # 画面からの入力値を個別で入力せず、POSTしてきた値をすべてModel(DB)に登録する場合
        entity = HelloModelMapper(request.POST, instance=Friend())
        entity.save()
        self.param["form"] = entity
        self.param["success_message"] = "作成完了"
        return redirect(to="hello_insert")
        # return render(request, "hello/insert.html", self.param)


class HelloEditView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "更新画面",
        }

    def get(self, request, entity_id):
        # ID検索
        entity = Friend.objects.get(id=entity_id)
        self.param["form"] = HelloModelMapper(instance=entity)
        self.param["entity_id"] = entity_id
        return render(request, "hello/edit.html", self.param)

    def post(self, request, entity_id):
        # ID検索
        friend = Friend.objects.get(id=entity_id)
        entity = HelloModelMapper(request.POST, instance=friend)
        entity.save()
        self.param["form"] = entity
        self.param["success_message"] = "更新完了"
        self.param["entity_id"] = entity_id
        return render(request, "hello/edit.html", self.param)


class HelloDeleteView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "削除画面",
        }

    def get(self, request, entity_id):
        # ID検索
        self.param["form"] = Friend.objects.get(id=entity_id)
        self.param["entity_id"] = entity_id
        return render(request, "hello/delete.html", self.param)

    def post(self, request, entity_id):
        # ID検索
        entity = Friend.objects.get(id=entity_id)
        entity.delete()
        self.param["form"] = None
        self.param["entity_id"] = entity_id
        self.param["success_message"] = "削除完了"
        return render(request, "hello/delete.html", self.param)


class HelloFindView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "詳細検索画面",
            "form": HelloFindForm()
        }

    def get(self, request):
        self.param["text"] = "検索したい単語を入力してください"
        self.param["form"] = HelloFindForm()
        self.param["entity_list"] = Friend.objects.all()
        return render(request, "hello/find.html", self.param)

    def post(self, request):
        self.param["text"] = "検索結果"
        self.param["form"] = HelloFindForm(request.POST)
        input_name = request.POST["name"]
        print("input_name=" + str(input_name))

        input_mail = request.POST["mail"]
        print("input_mail=" + str(input_mail))

        input_age = request.POST["age"]
        print("input_age=" + str(input_age))

        if input_name is not "":
            # 完全一致検索
            # self.param["entity_list"] = Friend.objects.filter(name=input_name)
            # 部分一致検索
            self.param["entity_list"] = Friend.objects.filter(name__contains=input_name)
            # 前方一致検索
            # self.param["entity_list"] = Friend.objects.filter(name__startswith=input_name)
            # 後方一致検索
            # self.param["entity_list"] = Friend.objects.filter(name__endswith=input_name)

        elif input_mail is not "":
            # 大文字小文字を区別しない検索
            # self.param["entity_list"] = Friend.objects.filter(mail__iexact=input_mail)
            # 大文字小文字を区別しない部分一致検索
            self.param["entity_list"] = Friend.objects.filter(mail__icontains=input_mail)
            # 大文字小文字を区別しない前方一致検索
            # self.param["entity_list"] = Friend.objects.filter(mail__istartswith=input_mail)
            # 大文字小文字を区別しない後方一致検索
            # self.param["entity_list"] = Friend.objects.filter(mail__iendswith=input_mail)

        elif input_age is not "":
            # 数値の比較
            # 完全一致
            # self.param["entity_list"] = Friend.objects.filter(age=input_age)
            # 値よりも大きい
            # self.param["entity_list"] = Friend.objects.filter(age__gt=input_age)
            # 値以上
            # self.param["entity_list"] = Friend.objects.filter(age__gte=input_age)
            # 値よりも小さい
            # self.param["entity_list"] = Friend.objects.filter(age__lt=input_age)
            # 値以下
            # self.param["entity_list"] = Friend.objects.filter(age__lte=input_age)

            # AND検索(10歳以上 かつ 20歳未満)
            # self.param["entity_list"] = Friend.objects.filter(age__gte=10, age__lt=20)
            # OR検索(10歳 または 20歳)
            # self.param["entity_list"] = Friend.objects.filter(Q(age=10) | Q(age=20))
            # IN検索(10歳 または 20歳 または 30歳)
            self.param["entity_list"] = Friend.objects.filter(age__in=[10, 20, 30])

        else:
            # 検索条件が指定されていない場合、全件検索
            self.param["entity_list"] = Friend.objects.all()

        return render(request, "hello/find.html", self.param)


class HelloValidView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "妥当性チェック画面",
            # form": ValidForm(),
            "form": HelloModelMapper(),
            "initialize_msg": "任意のメッセージを入力してください",
        }

    def get(self, request):
        # self.param["form"] = ValidForm()
        self.param["form"] = HelloModelMapper()
        return render(request, "hello/valid.html", self.param)

    def post(self, request):

        # form = ValidForm(request.POST)
        form = HelloModelMapper(request.POST, instance=Friend())
        self.param["form"] = form
        # form.save()
        if (form.is_valid()):
            # リクエスト値が正常の場合
            self.param["result_msg"] = "送信した値が正常です "

        else:
            # リクエスト値が不正の場合
            self.param["result_msg"] = "送信した値が不正です "

        print(self.param["result_msg"])
        return render(request, "hello/valid.html", self.param)


class HelloPagingView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "ページング画面",
        }

    def get(self, request, page_id=1):
        entity_list = Friend.objects.all()
        entity_list_perpage = Paginator(entity_list, 10)

        print("件数=" + str(len(entity_list)))
        print("page_id=" + str(page_id))

        self.param["entity_list"] = entity_list_perpage.get_page(page_id)

        return render(request, "hello/paging.html", self.param)


class MessageView(TemplateView):

    def __init__(self):
        self.param = {
            "title": "Message画面",
        }

    def get(self, request, page=1):
        # GET通信の場合

        print("MessageView_get")

        self.do_common_exec(page)
        return render(request, "hello/message.html", self.param)

    def post(self, request, page=1):
        # POST通信の場合

        print("MessageView_post")

        form = MessageForm(request.POST, instance=Message())
        form.save()

        self.do_common_exec(page)
        return render(request, "hello/message.html", self.param)

    def do_common_exec(self, page=1):

        message_entity_list = Message.objects.all().reverse()
        paginator = Paginator(message_entity_list, 10)

        m = {
            "form": MessageForm(),
            "message_entity_list": paginator.get_page(page)
        }
        # 既存のMapに追加
        self.param.update(m)
