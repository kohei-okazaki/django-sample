# -*- coding: utf-8 -*-
from django import forms
from django.forms import Form
"""
Created on 2020/05/06
各画面のForm
@author: okazaki
@version: 1.0.0
"""

"""
IndexのForm
"""


class IndexForm(Form):

    def __init__(self):
        pass


class RegistForm(Form):

    def __init__(self):
        pass

    # ID
    id = forms.IntegerField(label="ID")
    # パスワード
    password = forms.CharField(label="パスワード")
    # 確認用パスワード
    confirm_password = forms.CharField(label="確認用パスワード")
