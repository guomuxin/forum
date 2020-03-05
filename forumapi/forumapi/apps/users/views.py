from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_redis import get_redis_connection
from urllib.parse import urlencode
from urllib.request import urlopen
from rest_framework import status
from forumapi.utils.yuntongxun.sms import CCP
from forumapi.settings import constants
import json
import logging
import random

from django.conf import settings
from . import serializers
from .utils import get_user_by_data

from . import models

# Create your views here.

loger = logging.Logger("log")


class CaptchaAPIView(APIView):
    def post(self, request):
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
        return Response({"message": ret, "randstr": Randstr})

    def txrequest(self, appkey, params, m="GET"):
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
        if not user:
            return Response({"err_msg": "ok", "err_status": 1})
        else:
            return Response({"err_msg": "该手机号已注册", "err_status": 0}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCreateAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.RegisterModelSerializer



class SMSCodeAPIView(APIView):
    def get(self, request, mobile):
        redis = get_redis_connection("sms_code")
        if redis.get(f"interval{mobile}"):
            return Response({"messgae": "短信已在发送中,请问重复点击"}, status=status.HTTP_400_BAD_REQUEST)
        sms_code = "%04d" % random.randint(0, 9999)
        try:
            ccp = CCP()
            ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME // 60], constants.SMS_TEMPLATE_ID)
        except:
            ret = False
        if not ret:
            loger.error("发送短信失败!")
            # return Response("短信发送失败!")

        # 保存手机号及冷却时间到redis中
        redis.setex(mobile, constants.SMS_EXPIRE_TIME, sms_code)
        redis.setex(f"interval{mobile}", constants.SMS_INTERVAL_TIME, "yes")
        return Response({"message": "信息已发送,请注意查收"})
