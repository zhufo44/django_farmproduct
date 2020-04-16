from django.contrib import admin
from . import models


class PriceAdmin(admin.ModelAdmin):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class BaikeAdmin(admin.ModelAdmin):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class MarketAdmin(admin.ModelAdmin):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class StatuteAdmin(admin.ModelAdmin):
    list_display = ('title','pubtime','author')
    empty_value_display = '--'
    list_per_page = 50

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','c_time')
    empty_value_display = '--'
    list_per_page = 50

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('title','pubtime')
    empty_value_display = '--'
    list_per_page = 50

class SupplyAdmin(admin.ModelAdmin):
    list_display = ('title','price','pubtime')
    empty_value_display = '--'
    list_per_page = 50

admin.site.register(models.UserInfo,UserAdmin)
admin.site.register(models.Baike,BaikeAdmin)
admin.site.register(models.Market,MarketAdmin)
admin.site.register(models.Price,PriceAdmin)
admin.site.register(models.Statute,StatuteAdmin)
admin.site.register(models.Purchase,PurchaseAdmin)
admin.site.register(models.Supply,SupplyAdmin)


admin.site.site_title = '管理后台'
# 放在每个管理页面末尾的<title>，默认情况下是“Django站点管理员”
admin.site.site_header = '农产品信息物流平台'
# 放在每个管理页面顶部的<h1>文本，默认情况下是“Django管理”
admin.site.index_title = ''
# 管理员索引页面顶部的文本，默认情况下是“站点管理”
admin.site.site_url = '/index'
# 管理页面顶部“查看网站”链接的URL，默认情况下是/，将其设置None将删除链接