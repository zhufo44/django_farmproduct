from django.urls import path,include
from . import views


app_name = 'product'
urlpatterns = [
    path('supply/',views.supply),
    path('supdetail/<int:pk>/',views.supdetail,name='supdetail'),
    path('purcharse/',views.purcharse),
    path('purdetail/<int:pk>/', views.purdetail, name='purdetail'),
    # 价格详情
    path('price/',views.price,name='price'),
    path('price/<int:pk>/',views.pridetail,name='pridetail'),
    # 政策法规
    path('statute/',views.statute,name='statute'),
    path('statute/<int:pk>/',views.stadetail,name='stadetail'),
    # 农业百科
    path('baike/',views.baike,name='baike'),
    path('baike/<int:pk>/',views.baidetail,name='baidetail'),
    # 市场动态
    path('market/',views.market,name='market'),
    path('market/<int:pk>/',views.mardetail,name='mardetail'),
    # 车源信息
    path('vehicle/', views.vehicle, name='vehicle'),
    # path('vehicle/<int:pk>/', views.mardetail, name='vehdetail'),
    # 仓储信息
    path('storage/', views.storage, name='storage'),
    # path('storage/<int:pk>/', views.mardetail, name='stodetail'),
    # ajax
    path('pro/', views.pro),
    path('city<int:pid>/', views.city),
    path('product/', views.product),
    path('product<int:pid>/', views.product2)
]