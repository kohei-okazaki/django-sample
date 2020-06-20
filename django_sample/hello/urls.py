# -*- coding: utf-8 -*-
"""
Created on Mon May  4 18:21:17 2020

@author: okazaki
"""

from django.urls import path
from hello.views import HelloView, HelloListView, HelloInsertView, HelloEditView, HelloDeleteView, HelloFindView, \
    HelloValidView, HelloPagingView, MessageView

urlpatterns = [
    # 1
    # path("", views.index, name="index"),
    # 2
    # path("<int:id>/<nickname>/", views.index, name="index"),
    # 3
    # path("", views.index, name="index"),
    # 4
    # path("", views.index, name="index"),
    # path("next", views.next, name="next"),
    # 5
    # path("", views.index, name= "index"),
    # path("form", views.form, name= "form"),
    # 6
    # path("", views.index, name= "index"),
    # 7
    path(r"", HelloView.as_view(), name="hello_index"),
    # 8
    path(r"search", HelloListView.as_view(), name="hello_search"),
    path(r"search/<int:page>", HelloListView.as_view(), name="hello_search"),
    #
    path(r"insert", HelloInsertView.as_view(), name="hello_insert"),
    #
    path(r"edit/<int:entity_id>", HelloEditView.as_view(), name="hello_edit"),
    #
    path(r"delete/<int:entity_id>", HelloDeleteView.as_view(), name="hello_delete"),
    #
    path(r"find", HelloFindView.as_view(), name="hello_find"),
    #
    path(r"valid", HelloValidView.as_view(), name="hello_valid"),
    #
    path(r"paging", HelloPagingView.as_view(), name="hello_paging"),
    path(r"paging/<int:page_id>", HelloPagingView.as_view(), name="hello_paging"),

    #
    path(r"message/", MessageView.as_view(), name="message_index"),
    #
    path(r"message/<int:page>", MessageView.as_view(), name="message_index"),
]
