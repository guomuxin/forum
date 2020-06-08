from django.shortcuts import render
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
# Create your views here.

class BannerListAPIView(ListAPIView):
    queryset = models.Banner.objects.filter(is_show=True).order_by("orders")
    serializer_class = serializers.BannerModelSerializer

class NavHeaderListAPIView(ListAPIView):
    queryset = models.Nav.objects.filter(is_show=True, is_delete=False, option=1,pid=None).order_by("orders","-id")[:8]
    serializer_class = serializers.NavModelSerializer

class NavFooterListAPIView(ListAPIView):
    queryset = models.Nav.objects.filter(is_show=True, is_delete=False, option=2,pid=None).order_by("orders","-id")[:8]
    serializer_class = serializers.NavModelSerializer