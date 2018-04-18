#coding: utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import logging

def ServerView(request):
    if request.method == 'GET':
        return render(request, 'cmdb/idc.html')