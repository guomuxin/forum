from django.db import models
from forumapi.utils.models import BaseModel
# Create your models here.

class Banner(BaseModel):
    image = models.ImageField(upload_to='banner', verbose_name='轮播图', null=True, blank=True)
    note = models.CharField(max_length=150, verbose_name='备注信息')
    link = models.CharField(max_length=150, verbose_name='轮播图广告地址')
    is_http = models.BooleanField(verbose_name="是否为站内地址", default=True)

    class Meta:
        db_table = "ly_banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Nav(BaseModel):
    POSITION = (
        (1, "头部导航"),
        (2, "脚部导航")
    )
    is_http = models.BooleanField(default=True, verbose_name="是否站内的链接", help_text="如果是站内地址,则默认勾选")
    link = models.CharField(max_length=500, verbose_name='导航地址', help_text="如果是站外链接,必须加上协议, 格式如: http://www.renran.cn")
    pid = models.ForeignKey("Nav", related_name="son", null=True, blank=True, on_delete=models.DO_NOTHING,
                            verbose_name="父亲导航", )
    option = models.SmallIntegerField(choices=POSITION, default=1, verbose_name="导航位置")
    icon = models.CharField(max_length=100, verbose_name="图标", default="iconfont ic-navigation-notification menu-icon")

    class Meta:
        db_table = 'rr_nav'
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name

    @property
    def son_list(self):
        result = self.son.filter(is_show=True, is_delete=False).order_by("orders")
        data = []
        for item in result:
            data.append({
                'name': item.name,
                'link': item.link,
                'is_http': item.is_http
            })
        return data