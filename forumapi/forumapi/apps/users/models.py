from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=15, null=True, unique=True, help_text="手机号码", verbose_name="手机号码")
    nickname = models.CharField(max_length=15, null=True, unique=True, help_text="昵称", verbose_name="昵称")
    wxchat = models.CharField(max_length=100, null=True, unique=True, help_text="微信账号", verbose_name="微信账号")
    alipay = models.CharField(max_length=100, null=True, unique=True, help_text="支付宝账号", verbose_name="支付宝账号")
    qq_number = models.CharField(max_length=11, null=True, unique=True, help_text="QQ号", verbose_name="QQ号")
    # upload_to:保存文件的子目录
    avatar = models.ImageField(upload_to="avatar", null=True, default=None, verbose_name="头像")
    class Meta:
        db_table = 'forum_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username


