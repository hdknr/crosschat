# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return TemplateResponse(
        request, 'chat/index.html', dict(request=request,))


@login_required
def detail(request, id):
    return TemplateResponse(
        request, 'chat/detail.html', dict(request=request,))
