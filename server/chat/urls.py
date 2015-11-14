# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<id>\d+)', views.detail, name="chat_detail"),
    url(r'', views.index, name="chat_index"),
]
