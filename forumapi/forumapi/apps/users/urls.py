from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('captcha/', views.CaptchaAPIView.as_view()),
    re_path('^mobile/(?P<mobile>1[3-9]\d{9})/$', views.CheckMobileAPIView.as_view()),
    path('register/', views.RegisterCreateAPIView.as_view()),
    re_path('^sms/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeAPIView.as_view()),
]