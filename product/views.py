from django.shortcuts import render
from django.shortcuts import redirect
from . import forms
from .import models
import hashlib
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# 首页--需要返回6中数据
def index(request):
    prices = models.Price.objects.all()[:5]
    baikes = models.Baike.objects.all()[:5]
    statutes = models.Statute.objects.all()[:5]
    markets = models.Market.objects.all()[:5]
    supplys = models.Supply.objects.all()[:5]
    purcharses = models.Purchase.objects.all()[:5]
    context = {
        'supplys':supplys,
        'purcharses':purcharses,
        'prices':prices,
        'baikes':baikes,
        'statutes':statutes,
        'markets':markets
    }
    return render(request,'product/base.html',context=context)

def hash_code(s, salt='nong'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
# 注册
def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        # 根据post对象构建表单实例
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.UserInfo.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'product/login.html', {'login_form':login_form,'message':message})

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'product/login.html', {'login_form':login_form,'message':message})
        else:
            return render(request, 'product/login.html', {'login_form':login_form,'message':message})

    login_form = forms.UserForm()
    return render(request, 'product/login.html',{'login_form':login_form})

# 登录
def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            phone = register_form.cleaned_data.get('phone')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'product/register.html',{'register_form':register_form,'message':message})
            else:
                same_name_user = models.UserInfo.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'product/register.html', {'register_form':register_form,'message':message})
                same_email_user = models.UserInfo.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', {'register_form':register_form,'message':message})

                new_user = models.UserInfo()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.phone = phone
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'product/register.html', {'register_form':register_form,'message':message})
    register_form = forms.RegisterForm()
    return render(request, 'product/register.html',{'register_form':register_form})

# 注销
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/index/")



# 分页
def pagedata(articles,page,pagesize=10):
    p = Paginator(articles,pagesize)   #根据查询器生成page对象
    if p.num_pages <= 1:  #如果文章不足一页
        article_list = articles  #直接返回所有文章
        data = ''  #不需要分页按钮
    else:
        article_list = p.page(page) #返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False   # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  #如果请求第1页
            right = page_range[page:page+2]  #获取右边连续号码页
            if right[-1] < total_pages - 1:    # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:   # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  #如果请求最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]  #获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  #如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1: #如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  #如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]   #获取左边连续号码页
            right = page_range[page:page+2] #获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {    #将数据包含在data字典中
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
            'total_pages':total_pages,
            'page':page
        }

    return article_list,data

#============================================================================================
def supply(request):
    suplist = models.Supply.objects.all()
    page = int(request.GET.get('page', 1))
    suplist, data = pagedata(suplist, page,pagesize=16)
    context = {'suplist': suplist,'data':data}
    return render(request,'product/supply.html',context)


def supdetail(request,pk):
    odetail = models.Supply.objects.get(pk=pk)
    # 浏览量加一
    odetail.increase_views()
    # 返回浏览量前5个  表示热门产品
    sups = models.Supply.objects.order_by('-views')[:5]
    purs = models.Purchase.objects.order_by('-views')[:5]
    return render(request,'product/supdetail.html',{"odetail":odetail,"sups":sups,"purs":purs})

def purcharse(request):
    purlist = models.Purchase.objects.all()
    page = int(request.GET.get('page', 1))
    purlist, data = pagedata(purlist, page,pagesize=16)
    context = {'purlist':purlist,'data':data}
    return render(request,'product/purchase.html',context)
def purdetail(request,pk):
    odetail = models.Purchase.objects.get(pk=pk)
    # 浏览量加一
    odetail.increase_views()
    # 返回浏览量前5个  表示热门产品
    sups = models.Supply.objects.order_by('-views')[:5]
    purs = models.Purchase.objects.order_by('-views')[:5]
    return render(request,'product/purdetail.html',{"odetail":odetail,"sups":sups,"purs":purs})

# 政策法规
def statute(request):
    articles = models.Statute.objects.all()
    page = int(request.GET.get('page', 1))
    articlelist, data = pagedata(articles, page)
    context = {'articlelist': articlelist, 'data': data}
    return render(request, 'product/statute.html', context=context)
# 文章详情
def stadetail(request, pk):
    article = models.Statute.objects.get(pk=pk)
    return render(request, 'product/stadetail.html', {'article': article})

# 农业百科
def baike(request):
    articles = models.Baike.objects.all()
    page = int(request.GET.get('page', 1))
    articlelist, data = pagedata(articles, page)
    context = {'articlelist': articlelist, 'data': data}
    return render(request, 'product/baike.html', context=context)
    # 文章详情
def baidetail(request, pk):
    article = models.Baike.objects.get(pk=pk)
    return render(request, 'product/baidetail.html', {'article': article})

# 市场动态
def market(request):
    articles = models.Market.objects.all()
    page = int(request.GET.get('page', 1))
    articlelist, data = pagedata(articles, page)
    context = {'articlelist': articlelist, 'data': data}
    return render(request, 'product/market.html', context=context)
# 文章详情
def mardetail(request, pk):
    article = models.Market.objects.get(pk=pk)
    return render(request, 'product/mardetail.html', {'article': article})

# 价格行情
def price(request):
    articles = models.Price.objects.all()
    page = int(request.GET.get('page', 1))
    articlelist,data = pagedata(articles,page)
    context = {'articlelist':articlelist,'data':data}
    return render(request,'product/price.html',context=context)
# 文章详情
def pridetail(request,pk):
    article = models.Price.objects.get(pk=pk)
    return render(request,'product/pridetail.html',{'article':article})


# 车源信息
def vehicle(request):
    articles = models.Vehicle.objects.all()
    page = int(request.GET.get('page', 1))
    articlelist,data = pagedata(articles,page)
    context = {'articlelist':articlelist,'data':data}
    return render(request,'product/vehicle.html',context=context)


# 仓储信息
def storage(request):
    articles = models.Storage.objects.all()
    page = int(request.GET.get('page', 1))
    articlelist,data = pagedata(articles,page)
    context = {'articlelist':articlelist,'data':data}
    return render(request,'product/storage.html',context=context)

# 我要发布 -- 供应和采购共同使用该函数
def publish(request):
    # 如果没有登录 直接跳转至登录页面
    if not request.session.get('is_login',None):
        return redirect('/login/')

    # 如果是post存储数据
    if request.method == 'POST':
        # 通过判断参数file是否存在图片 判断是供应还是采购
        datadict = request.POST.dict()
        print(datadict)
        # 共同部分
        title = datadict.get('title')
        cate1 = datadict.get('product1')
        cate2 = datadict.get('product2')
        pro = datadict.get('pro')
        city = datadict.get('city')
        dis = datadict.get('dis',None)
        address = datadict.get('address')
        detail = datadict.get('detail')

        # 查询外键
        user_id = request.session.get('user_id')
        userobject = models.UserInfo.objects.get(pk=user_id)

        cate1 = models.Category.objects.get(pk=cate1)
        cate2 = models.Category.objects.get(pk=cate2)
        pro = models.AreaInfo.objects.get(pk=pro)
        city = models.AreaInfo.objects.get(pk=city)
        dis = models.AreaInfo.objects.get(pk=dis) if dis!='0' else ''

        if 'file' in datadict.keys():
            # 说明是供应--多出  图片（可以为空）和 价格
            price = datadict.get('price')
            img_obj = request.FILES.get('file')

            supobject = models.Supply()
            supobject.price = price
            supobject.img = img_obj
            # 存储
            supobject.title = title
            supobject.detail = detail
            supobject.address = address
            supobject.region = pro.title + '-' + city.title + '-' + dis.title if dis else ''
            supobject.category = cate1.title + '-' + cate2.title
            # 存储外键
            supobject.supplys = userobject
            supobject.save()
            for data in cate1,cate2:
                if data:
                    supobject.supcate.add(data)
            for data in pro, city, dis:
                if data:
                    supobject.supregion.add(data)
        else:
            purobject = models.Purchase()
            # 存储
            purobject.title = title
            purobject.detail = detail
            purobject.address = address
            purobject.region = pro.title + '-' + city.title + '-' + dis.title if dis else ''
            purobject.category = cate1.title + '-' + cate2.title
            # 存储外键
            purobject.purchases = userobject
            purobject.save()
            for data in cate1,cate2:
                if data:
                    purobject.purcate.add(data)
            for data in pro,city,dis:
                if data:
                    purobject.purregion.add(data)

    return render(request,'product/publish.html')


# ajax
def pro(request):
    prolist = models.AreaInfo.objects.filter(parent__isnull=True)
    # 得到的dataset是一个列表，需要构造一个json数据
    plist = []
    for item in prolist:
        plist.append([item.id,item.title])
    data = {'data':plist}
    return JsonResponse(data)

def city(request,pid):
    citylist = models.AreaInfo.objects.filter(parent_id=pid)
    clist = []
    for item in citylist:
        clist.append({'id':item.id,'title':item.title})
    return JsonResponse({'data':clist})


def product(request):
    productlist = models.Category.objects.filter(parent__isnull=True)
    plist = []
    for item in productlist:
        plist.append([item.id,item.title])
    data = {'data':plist}
    return JsonResponse(data)

def product2(request,pid):
    productlist = models.Category.objects.filter(parent_id=pid)
    plist = []
    for item in productlist:
        plist.append({'id':item.id,'title':item.title})
    return JsonResponse({'data':plist})

# 用户中心
def userinfo(request):
    # 如果没有登录 直接跳转至登录页面
    if not request.session.get('is_login',None):
        return redirect('/login/')

    # 获取当前用户信息
    userID = request.session['user_id']
    user = models.UserInfo.objects.get(pk=userID)

    return render(request,'product/userinfo.html',{'user':user})

# 短信接收
def message(request):
    condict = {}
    if request.method == "GET":
        datadict = request.GET.dict()
        phone = datadict.get('phone')
        content = datadict.get('content')

        # 判断手机号 是否在数据库中
        if phone:
            try:
                user = models.UserInfo.objects.get(phone=phone)
                print(phone,user)

                # 存在手机号 处理content
                if content:
                    if content.startswith('*1*') and content.endswith('*1*'):
                        supobject = models.Supply()
                        # 表示 发布供应
                        content = content.replace('*1*', '').strip().split('；')
                        for text in content:
                            if text:
                                head,detail = text.split('：')
                                condict[head] = detail

                        supobject.supplys = user
                        supobject.title = condict.get('标题')
                        supobject.price = condict.get('报价')
                        supobject.detail = condict.get('描述')
                        supobject.address = condict.get('详细地址')
                        supobject.region = condict.get('所在地区')
                        supobject.category = condict.get('产品品种')
                        supobject.save()

                    elif content.startswith('*2*') and content.endswith('*2*'):
                        purobject = models.Purchase()
                        # 表示 发布采购
                        content = content.replace('*2*', '').strip().split('；')
                        for text in content:
                            if text:
                                head,detail = text.split('：')
                                condict[head] = detail

                        purobject.title = condict.get('标题')
                        purobject.detail = condict.get('描述')
                        purobject.address = condict.get('详细地址')
                        purobject.region = condict.get('所在地区')
                        purobject.category = condict.get('产品品种')
                        purobject.purchases = user
                        purobject.save()
                    else:
                        print('格式不对',content)

            except ObjectDoesNotExist:
                print('该手机号码没有注册',phone)

    return HttpResponse('request OK')

# 我的供应
def mysupply(request):
    userID = request.session['user_id']
    user = models.UserInfo.objects.get(pk=userID)

    # 查找该用户的所有供应--反向查询
    supplys = user.supply_set.all()

    return render(request,'product/mysupply.html',{"supplys":supplys})

# 我的采购
def mypurchase(request):
    userID = request.session['user_id']
    user = models.UserInfo.objects.get(pk=userID)

    # 查找该用户的所有采购--反向查询
    purchases = user.purchase_set.all()

    return render(request,'product/mypurchase.html',{'purchases':purchases})


def alterinfo(request):
    return HttpResponse('request ok')


def delete(request,keywords):
    if keywords.startswith('supply'):
        pk = keywords.replace('supply','')

        supobject = models.Supply.objects.get(pk=pk)
        supobject.delete()

        return HttpResponse('ok')

    if keywords.startswith('purchase'):
        pk = keywords.replace('purchase','')

        purobject = models.Purchase.objects.get(pk=pk)
        purobject.delete()

        return HttpResponse('ok')



import requests
from lxml import etree

def wandou(request):


    url = 'https://web.53seo.cn/'
    res = requests.get(url)
    html = etree.HTML(res.content.decode('utf8'))

    idlist = []
    alis = html.xpath("//div[@id='focuspic']//li/a")
    for ali in alis:
        idlist.append(ali.get('href'))

    streamlist = []

    for ids in idlist:
        ids = str(ids).replace('/', '')
        url = 'https://web.53seo.cn/index.php?g=home&m=show&a=setNodeInfo&showid={}&stream={}_{}'.format(ids, ids,
                                                                                                              ids)
        res = requests.get(url).json()
        streamlist.append(res['userinfo']['stream'])

    urllist = []
    for stream in streamlist:
        ids = str(stream.split('_')[0])
        url = 'https://web.53seo.cn/index.php?g=home&m=Show&a=checkLive&liveuid={}&stream={}'.format(ids, stream)

        res = requests.get(url).json()
        if res.get('type') == '2':
            # text = 'https://pull.sn00.org/live/{}.flv'.format(stream)
            urllist.append(stream)


    return render(request,'wandou/index.html',{'urllist':urllist})




def wandou2(request,keywords):

    text = 'https://pull.sn00.org/live/{}.flv'.format(keywords)

    html = '<embed src="http://www.3464.com/tools/FLVLyplayer/Lyplayer.swf?path={}&type=flv&fullscreen=true&autoplay=true&backcolor=99ff33&frontcolor=ffffff" type="application/x-shockwave-flash" width="550" height="400" quality="high" allowFullscreen="true" />'.format(text)

    return HttpResponse(html)
