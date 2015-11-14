# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

from . import models


@login_required
def index(request):
    rooms = models.Room.objects.filter(topicuser__user__user=request.user)
    return TemplateResponse(
        request, 'chat/index.html',
        dict(request=request, rooms=rooms))


@login_required
def detail(request, id):
    host = request.META.get('HTTP_HOST', '').split(':')[0]
    port = 8080
    return TemplateResponse(
        request, 'chat/detail.html',
        dict(request=request,
             room=models.Room.objects.get(id=id),
             wsuri="ws://{0}:{1}/ws".format(host, port),))
