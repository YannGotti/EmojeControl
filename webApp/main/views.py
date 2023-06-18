from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.base import View
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


class MainPage(View):
    def get(self, request):
        return render(request, 'main/index.html')

