from django.db import models
from mdeditor.fields import MDTextField
import uuid

# 自定义图片路径
def image_upload_to(instance, filename):
    return 'img/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)



# 省市区三级
class AreaInfo(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 产品分类
class Category(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 用户信息表
class UserInfo(models.Model):
    # 默认第一个参数 verbose
    name = models.CharField('用户名',max_length=20,unique=True)
    password = models.CharField('密码',max_length=128)
    email = models.EmailField('邮箱',unique=True)
    phone = models.CharField('手机号',max_length=11, unique=True)
    c_time = models.DateTimeField('创建时间',auto_now_add=True)
    # 用户可以发布 供应和求购  外键定义在多的一方

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户列表"
        verbose_name_plural = "用户列表"


# 供应产品
class Supply(models.Model):
    title = models.CharField('标题',max_length=30)
    price = models.CharField('最新报价',max_length=20)
    pubtime = models.DateField('发布时间',auto_now_add=True)
    region = models.CharField('地区',max_length=50)
    address = models.CharField('详细地址',max_length=30)
    views = models.PositiveIntegerField('浏览量',default=0)
    category = models.CharField('产品类别',max_length=30)
    detail = models.TextField('详细描述')
    # 图片
    img = models.ImageField(verbose_name='图片',upload_to=image_upload_to,null=True,)

    # 外键关联用户
    supplys = models.ForeignKey(UserInfo,on_delete=models.CASCADE,verbose_name='用户')

    # 多对多外键
    supregion = models.ManyToManyField(AreaInfo,verbose_name='地区筛选')
    supcate = models.ManyToManyField(Category,verbose_name='品种筛选')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "供应信息"
        verbose_name_plural = "供应信息"


# 求购产品
class Purchase(models.Model):
    title = models.CharField('标题',max_length=30)
    pubtime = models.DateField('发布日期',auto_now_add=True)
    # 地区 选择器
    region = models.CharField('地区',max_length=50)
    address = models.CharField('详细地址',max_length=30)
    views = models.PositiveIntegerField('浏览量',default=0)
    # 分类 选择器
    category = models.CharField('产品类别',max_length=30)
    detail = models.TextField('详细描述',)
    # 外键关联用户
    purchases = models.ForeignKey(UserInfo,on_delete=models.CASCADE,verbose_name='用户')

    # 多对多外键
    purregion = models.ManyToManyField(AreaInfo,verbose_name='地区筛选')
    purcate = models.ManyToManyField(Category,verbose_name='品种筛选')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "求购信息"
        verbose_name_plural = "求购信息"

# 以下内容与用户无关，由管理员定义
# ====================================================================================================
# 价格行情
class Price(models.Model):
    title = models.CharField('标题',max_length=30)
    pubtime = models.DateField('发布日期',)
    author = models.CharField('作者',max_length=30,blank=True)
    source = models.CharField('来源',max_length=30)
    content = MDTextField('文章')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "价格行情"
        verbose_name_plural = "价格行情"

# 市场动态
class Market(models.Model):
    title = models.CharField('标题',max_length=30)
    pubtime = models.DateField('发布日期',)
    author = models.CharField('作者',max_length=30,blank=True)
    source = models.CharField('来源',max_length=30)
    content = models.TextField('文章')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "市场动态"
        verbose_name_plural = "市场动态"

# 农业百科
class Baike(models.Model):
    title = models.CharField('标题',max_length=30)
    pubtime = models.DateField('发布日期',)
    author = models.CharField('作者',max_length=30,blank=True)
    source = models.CharField('来源',max_length=30)
    content = models.TextField('文章')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "农业百科"
        verbose_name_plural = "农业百科"


# 政策法规
class Statute(models.Model):
    title = models.CharField('标题',max_length=30)
    pubtime = models.DateField('发布日期',)
    author = models.CharField('作者',max_length=30,blank=True)
    source = models.CharField('来源',max_length=30)
    content = models.TextField('文章')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "政策法规"
        verbose_name_plural = "政策法规"


# 车源信息
class Vehicle(models.Model):
    number = models.CharField('车牌号',max_length=30)
    type = models.CharField('类型',max_length=10)
    load = models.CharField('载重',max_length=30)
    address = models.CharField('所在城市',max_length=30)
    people = models.CharField('联系人',max_length=30)
    phone = models.CharField('联系电话',max_length=30)
    pubtime = models.DateField('发布日期')
    def __str__(self):
        return self.number
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "车源信息"
        verbose_name_plural = "车源信息"

# 仓储信息
class Storage(models.Model):
    type = models.CharField('仓库类型',max_length=10)
    pubtime = models.DateField('发布日期',)
    address = models.CharField('所在城市',max_length=30)
    area = models.CharField('仓库面积',max_length=30)
    price = models.CharField('每间价格',max_length=30)
    people = models.CharField('联系人',max_length=30,default='')
    phone = models.CharField('联系电话',max_length=30,default='')

    def __str__(self):
        return self.type
    class Meta:
        ordering = ["-pubtime"]
        verbose_name = "仓储信息"
        verbose_name_plural = "仓储信息"
