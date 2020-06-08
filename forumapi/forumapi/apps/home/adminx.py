import xadmin
from xadmin import views
from . import models


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


# xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "forum"  # 设置站点标题
    site_footer = "forum"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


# xadmin.site.register(views.CommAdminView, GlobalSettings)


class BannerModelAdmin(object):
    list_display = ["id", "name", "link", "is_show", 'is_http']
    list_editable = ["is_show", 'is_http']

xadmin.site.register(models.Banner, BannerModelAdmin)

class NavModelAdmin(object):
    list_display = ["id", "name", "link", "is_show", 'is_http', "created_time", "updated_time"]
    list_editable = ["is_show", 'is_http', "created_time", "updated_time"]
xadmin.site.register(models.Nav, NavModelAdmin)