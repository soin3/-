from django.db import models
from django.contrib.auth.models import User


class Host(models.Model):
    '''主机表'''
    name =  models.CharField(verbose_name='主机名',max_length=64,unique=True)
    ip_addr =  models.GenericIPAddressField(verbose_name='主机ip',unique=True)
    host_groups = models.ManyToManyField('HostGroup',verbose_name='主机组',blank=True)
    templates = models.ManyToManyField("Template",verbose_name='模板',blank=True)
    monitored_by_choices = (
        (1,'Agent'),
        (2,'SNMP'),
        (3,'WGET'),
    )
    monitored_by = models.CharField(verbose_name='监控方式',max_length=64,choices=monitored_by_choices)
    status_choices= (
        (1,'在线'),
        (2,'离线'),
        (3,'未知'),
        (4,'故障'),
    )
    host_alive_check_interval = models.IntegerField(verbose_name="主机存活状态检测间隔", default=30)
    status = models.IntegerField(verbose_name='状态',choices=status_choices,default=1)
    memo = models.TextField(verbose_name="备注",blank=True,null=True)
    enabled = models.BooleanField(verbose_name='是否需要监控',default=True)

    def __str__(self):
        return self.name

class HostGroup(models.Model):
    name = models.CharField(verbose_name='主机组名称',max_length=64,unique=True)
    templates = models.ManyToManyField("Template",verbose_name='模板',blank=True)
    memo = models.TextField(verbose_name="备注",blank=True,null=True)

    def __str__(self):
        return self.name

class ServiceIndex(models.Model):
    '''存储主机服务的指标信息'''
    name = models.CharField(max_length=64)
    key =models.CharField(max_length=64,unique=True)#真正的指标名
    data_type_choices = (
        (1,"int"),
        (2,"float"),
        (3,"string")
    )
    data_type = models.CharField(verbose_name='指标数据类型',max_length=32,choices=data_type_choices,default=1)
    memo = models.CharField(verbose_name="备注",max_length=128,blank=True,null=True)

    def __str__(self):
        return "%s.%s" %(self.name,self.key)

class Service(models.Model):
    '''主机服务表'''
    name = models.CharField(verbose_name='服务名称',max_length=64,unique=True)
    interval = models.IntegerField(verbose_name='监控间隔',default=60)
    plugin_name = models.CharField(verbose_name='插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('ServiceIndex',verbose_name="指标列表",blank=True)
    has_sub_service = models.BooleanField(default=False,help_text=u"如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡")
    memo = models.CharField(verbose_name="备注",max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    '''一个模板存储多个服务'''
    name = models.CharField(verbose_name='模版名称',max_length=64,unique=True)
    services = models.ManyToManyField('Service',verbose_name="服务列表")
    #triggers = models.ManyToManyField('Trigger',verbose_name=u"触发器列表",blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64,blank=True,null=True)

    def __str__(self):
        return self.name




