import xadmin
from . import models


class PriceAdmin(object):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class BaikeAdmin(object):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class MarketAdmin(object):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class StatuteAdmin(object):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class UserAdmin(object):
    list_display = ('name','email','c_time')
    empty_value_display = '--'
    list_per_page = 50

class PurchaseAdmin(object):
    list_display = ('title','pubtime')
    empty_value_display = '--'
    list_per_page = 50

class SupplyAdmin(object):
    list_display = ('title','price','pubtime')
    empty_value_display = '--'
    list_per_page = 50

class StorageAdmin(object):
    list_display = ('type','price','pubtime')
    empty_value_display = '--'
    list_per_page = 50

class VehicleAdmin(object):
    list_display = ('number','type','pubtime')
    empty_value_display = '--'
    list_per_page = 50

from xadmin import views

class GlobalSetting(object):

    # 设置后台顶部标题
    site_title ='农产品物流平台'
    # 设置后台底部标题
    site_footer =' 农产品公共信息物流平台'

xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(models.UserInfo,UserAdmin)
xadmin.site.register(models.Baike,BaikeAdmin)
xadmin.site.register(models.Market,MarketAdmin)
xadmin.site.register(models.Price,PriceAdmin)
xadmin.site.register(models.Statute,StatuteAdmin)
xadmin.site.register(models.Storage,StorageAdmin)
xadmin.site.register(models.Vehicle,VehicleAdmin)
xadmin.site.register(models.Purchase,PurchaseAdmin)
xadmin.site.register(models.Supply,SupplyAdmin)

