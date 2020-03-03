import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import get_user_by_data


class RegisterModelSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True, label="jwt_token")
    sms_code = serializers.CharField(write_only=True, max_length=4, min_length=4, label="手机验证码")

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'nickname', 'mobile', 'sms_code', 'token', 'avatar', 'password']
        read_only_fields = ['id', 'username']
        extra_kwargs = {
            'mobile': {"write_only": True},
            'password': {"write_only": True, "min_length": 6, "max_length": 16},
        }

    def validate(self, attrs):
        # 验证手机号格式是否正确
        if not re.match("1[3-9]\d{9}", attrs.get("mobile")):
            raise serializers.ValidationError("手机号码格式错误")

        # 验证手机号是否被注册
        if get_user_by_data(mobile=attrs.get("mobile")):
            raise serializers.ValidationError("手机号已被注册")
        return attrs

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(
                username="用户" + validated_data.get("mobile")[-4:],
                password=validated_data.get("password"),
                nickname=validated_data.get("nickname"),
                mobile=validated_data.get("mobile"),
            )
        except:
            raise serializers.ValidationError("用户注册失败!")
        from rest_framework_jwt.settings import api_settings

        # 首次注册,免登录,手动生成jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user
