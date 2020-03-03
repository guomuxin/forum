from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from urllib.parse import urlencode
from urllib.request import urlopen
from rest_framework import status
import json

from django.conf import settings
from . import serializers
from .utils import get_user_by_data

from . import models
# Create your views here.

class CaptchaAPIView(APIView):
    def post(self,request):
        AppSecretKey = settings.TENCENT_CAPTCHA.get("App_Secret_Key")
        appid = settings.TENCENT_CAPTCHA.get("APPID")
        Ticket = request.data.get("ticket")
        Randstr = request.data.get("randstr")
        UserIP = request._request.META.get("REMOTE_ADDR")
        params = {
            "aid": appid,
            "AppSecretKey": AppSecretKey,
            "Ticket": Ticket,
            "Randstr": Randstr,
            "UserIP": UserIP
        }
        params = urlencode(params)

        ret = self.txrequest(AppSecretKey, params)
        return Response({"message":ret, "randstr":Randstr})

    def txrequest(self,appkey, params, m="GET"):
        url = "https://ssl.captcha.qq.com/ticket/verify"
        if m == "GET":
            f = urlopen("%s?%s" % (url, params))
        else:
            f = urlopen(url, params)

        content = f.read()
        res = json.loads(content)
        if not res:
            return False
        else:
            error_code = res["response"]
            if error_code == "1":
                return True
            else:
                # 记录日志
                loger.error("验证接口异常!%s:%s" % (res["response"], res["err_msg"]))

class CheckMobileAPIView(APIView):
    def get(self, request, mobile):
        user = get_user_by_data(mobile=mobile)
        print(user)
        if not user:
            return Response({"err_msg": "ok", "err_status": 1})
        else:
            return Response({"err_msg": "该手机号已注册", "err_status": 0}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCreateAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.RegisterModelSerializer
