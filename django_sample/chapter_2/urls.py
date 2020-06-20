# -*- coding: utf-8 -*-
'''
Created on 2020/05/06
リクエストURLとViewのマッピング
@author: okazaki
'''

from django.urls import path
from .views import IndexView, InputView, ConfirmView, CompleteView

urlpatterns = [
    # Index画面のViewを登録
    path(r"index", IndexView.as_view(), name="index"),
    # 登録画面のViewを登録
    path(r"input", InputView.as_view(), name="input"),
    # 登録情報入力確認画面のViewを登録
    path(r"confirm", ConfirmView.as_view(), name="confirm"),
    # 登録完了画面のViewを登録
    path(r"complete", CompleteView.as_view(), name="complete"),
]
