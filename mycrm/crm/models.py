from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

# Create your models here.
class Customer(models.Model):
    '''客户信息表：
    主要给销售人员用，存储所有客户信息，里面要记录客户来源＼姓名＼qq＼客户来源＼咨询的内容等,
    客户只要没报名，你没理由要求人家必须告诉你真实姓名及其它更多私人信息呀'''
    name = models.CharField(verbose_name="姓名",max_length=32,blank=True,null=True,help_text='用户报名后请改为真实姓名')
    #客户在咨询时，多是通过qq,所以这里就把qq号做为唯一标记客户的值，不能重复
    qq = models.CharField(verbose_name="qq号",max_length=64,unique=True,help_text=u'QQ号必须唯一')
    qq_name = models.CharField(verbose_name="qq名称",max_length=64,blank=True,null=True)
    id_num = models.CharField(verbose_name="身份证",max_length=64,blank=True,null=True)
    email = models.EmailField(verbose_name="邮箱",max_length=64,blank=True,null=True)
    source_choices = ((0,'转介绍'),
                      (1,'qq'),
                      (2,'微信'),
                      (3,'官方论坛'),
                      (4,'网上搜索'),
                      (5,'其他'),
                    )
    #这个客户来源渠道是为了以后统计各渠道的客户量＼成单量，先分类出来
    source = models.SmallIntegerField(verbose_name="来源",choices=source_choices)
    referral_from = models.CharField(verbose_name="转介绍人qq",max_length=64,blank=True,null=True)
    #已开设的课程单独搞了张表，客户想咨询哪个课程，直接在这里关联就可以
    consult_course = models.ForeignKey("Course",verbose_name="咨询课程",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="咨询详情")
    #课程顾问很得要噢，每个招生老师录入自己的客户
    tags = models.ManyToManyField("Tag",blank=True,verbose_name="标签",)
    consultant = models.ForeignKey("UserProfile",verbose_name="课程顾问",on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="咨询日期",auto_now_add=True)
    status_choices = ((0,"未报名"),
                      (1,"已报名")
                      )
    status = models.IntegerField(verbose_name="报名状态",default=0,choices=status_choices,help_text="选择客户此时的状态")

    def __str__(self):
        return "QQ:%s,Name:%s" %(self.qq,self.name)

    class Meta:
        verbose_name = "Customer客户信息表"
        verbose_name_plural = "Customer客户信息表"
        ordering = ['id']

class Tag(models.Model):
    '''标签'''
    name = models.CharField(unique=True,max_length=32)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag标签"
        verbose_name_plural = "Tag标签"
class CustomerFollowUp(models.Model):
    '''存储客户的后续跟进信息,客户跟进表，这张表的意义很容易理解， 一个客户今天咨询后，
    你录入到了客户信息表，但他没报名， 所以过了一段时间，销售还得再跟他聊聊吧，聊完后，
    结果又没报，那也得纪录下来吧，因为每个销售每天要聊很多人，你不纪录的话， 可能下次再跟这个人聊时，
    你早已忘记上次聊了什么了， 这样会让客户觉得这个销售不专业，相反，如果把每次跟进的内容都纪录下来，
    过了几个月，这个客户再跟你聊时，竟然发现，你还记得他的所有情况，他就觉得你很重视他，说不定一感动就报名了，
    哈哈。 所以，一条客户信息可能会对应多条跟进记录，是个1对多的关系，必须单独搞张表来记录'''
    customer = models.ForeignKey("Customer",verbose_name="所咨询客户",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile",verbose_name="跟踪人",on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="跟进日期",auto_now_add=True)
    status_choices = ((1,"近期无报名计划"),
                      (2,"2个月内报名"),
                      (3,"1个月内报名"),
                      (4,"2周内报名"),
                      (5,"1周内报名"),
                      (6,"2天内报名"),
                      (7,"已报名"),
                      (8,"已交全款"),
                      )
    status = models.IntegerField(verbose_name="状态",choices=status_choices,help_text="选择客户此时的状态")

    def __str__(self):
        return "QQ:%s -- Status:%s" %(self.customer.qq,self.status)

    class Meta:
        verbose_name = "CustomerFollowUp客户跟进表"
        verbose_name_plural = "CustomerFollowUp客户跟进表"

class Enrollment(models.Model):
    '''存储已报名学员的信息,这里为什么要把客户信息表 和 这个学员报名表分开呢？ 因内一个学员可以报多个课程 ，每个课程 都需要单独记录学习成绩呀什么的，
        ,所以每报一个课程 ，就在这里生成 一条相应的报名记录'''
    #所有报名的学生 肯定是来源于客户信息表的，先咨询，后报名嘛
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)
    consultant = models.ForeignKey("UserProfile",verbose_name="课程顾问",on_delete=models.CASCADE)
    contract_agreed = models.BooleanField("学员已同意合同",default=0)
    contract_approved = models.BooleanField("审批通过", help_text="合同已审核",default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.enrolled_class)

    class Meta:
        # #这里为什么要做个unique_together联合唯一？因为老男孩有很多个课程， 学生学完了一个觉得好的话，以后还可以再报其它班级，
        #每报一个班级，就得单独创建一条报名记录，所以这里想避免重复数据的话，就得搞个"客户 + 班级"的联合唯一喽
        unique_together = ('customer','enrolled_class')
        verbose_name = "Enrollment学员报名表"
        verbose_name_plural ="Enrollment学员报名表"

class ClassList(models.Model):
    '''存储班级信息,学生以班级为单位管理，这个表被学员表反向关联， 即每个学员报名时需要选择班级'''
    branch = models.ForeignKey("Branch",verbose_name="校区",on_delete=models.CASCADE)
    course = models.ForeignKey("Course",verbose_name="课程",on_delete=models.CASCADE)
    class_type_choices = ((0,'面授(脱产)'),(1,'面授(周末)'),(2,'随到随学网络'))
    class_type = models.SmallIntegerField(choices=class_type_choices,default=0,verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期",blank=True,null=True)
    contract = models.ForeignKey("Contract",blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s"%(self.branch,self.course,self.semester)

    class Meta:
        verbose_name = "ClassList班级表"
        verbose_name_plural ="ClassList班级表"

class Contract(models.Model):
    '''合同表'''
    name = models.CharField("合同名称",max_length=64,unique=True)
    template = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = " Contract合同表"
        verbose_name_plural ="Contract合同表"

class Course(models.Model):
    '''存储所开设课程的信息'''
    name = models.CharField(verbose_name="课程名",max_length=64,unique=True)
    price = models.PositiveSmallIntegerField(verbose_name="课程价格")
    outline = models.TextField(verbose_name="课程大纲")
    period  = models.IntegerField(verbose_name="课程周期(Month)")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Course课程信息表"
        verbose_name_plural ="Course课程信息表"


class CourseRecord(models.Model):
    '''存储各班级的上课记录,'''
    #每个班级都要上很多次课，讲师每上一次课的纪录都要纪录下来，以后可以方便统计讲师工资什么的
    from_class = models.ForeignKey("ClassList",verbose_name="班级",on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节课（天）")
    teacher = models.ForeignKey("UserProfile", verbose_name="讲师",on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(max_length=128,blank=True,null=True,verbose_name="作业标题")
    homework_content = models.TextField(blank=True,null=True,verbose_name="作业内容")
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateTimeField(verbose_name="上课日期",auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.from_class,self.day_num)

    class Meta:
        unique_together = ('from_class','day_num')
        verbose_name = "CourseRecord上课记录表"
        verbose_name_plural ="CourseRecord上课记录表"

class StudyRecord(models.Model):
    '''存储所有学员的详细的学习成绩情况'''
    student = models.ForeignKey("Enrollment",verbose_name="学员",on_delete=models.CASCADE)
    course_record = models.ForeignKey("CourseRecord", verbose_name="第几天课程",on_delete=models.CASCADE)
    record_choices = ((0,"已签到"),
                      (1,"迟到"),
                      (2,"缺勤"),
                      (3,"早退"),
                      )
    record = models.IntegerField(verbose_name="上课纪录",choices=record_choices,default=0,max_length=64)
    score_choices = ((100, 'A+'),   (90,'A'),
                     (85,'B+'),     (80,'B'),
                     (70,'B-'),     (60,'C+'),
                     (50,'C'),      (40,'C-'),
                     (-50,'D'),       (0,'N/A'),
                     (-100,'COPY'), (-1000,'FAIL'),
                     )
    score = models.IntegerField(verbose_name="本节成绩",choices=score_choices,default=0)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(verbose_name="备注",max_length=255,blank=True,null=True)

    def __str__(self):
        return "%s %s %s" %(self.student,self.course_record,self.score)

    class Meta:
        #一个学员，在同一节课只可能出现一次，所以这里把course_record ＋ student 做成联合唯一
        unique_together = ('course_record','student')
        verbose_name = "StudyRecord学习成绩表"
        verbose_name_plural ="StudyRecord学习成绩表"

# class UserProfile(models.Model):
#     '''账号表，这里我们用django自带的认证系统，并对其进行自定制'''
#     user = models.OneToOneField(User,on_delete=models.CASCADE,)
#     name = models.CharField(max_length=32,verbose_name="用户姓名")
#     roles = models.ManyToManyField("Role",blank=True,verbose_name="用户角色")
#
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name = "UserProfile账号表"
#         verbose_name_plural ="UserProfile账号表"
class UserProfileManager(BaseUserManager):
    #创建用户的方法
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''账号表'''
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
        )
    password = models.CharField(_('password'),max_length=128,help_text=mark_safe('''<a href="password/">修改密码</a>'''))
    name = models.CharField(max_length=32,verbose_name="用户姓名")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    roles = models.ManyToManyField("Role",blank=True)
    objects = UserProfileManager()
    stu_account = models.ForeignKey("Customer",verbose_name="学员账号",blank=True,null=True,help_text="只有学员报名后才能创建",on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Payment(models.Model):
    '''缴费记录'''
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE,verbose_name="缴费人")
    course = models.ForeignKey("Course",on_delete=models.CASCADE,verbose_name="所报课程")
    paid_fee = models.IntegerField(verbose_name="费用数额", default=0)
    note = models.TextField("备注",blank=True, null=True)
    date = models.DateTimeField("交款日期", auto_now_add=True)
    consultant = models.ForeignKey("UserProfile", verbose_name="负责老师", help_text="谁签的单就选谁",on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" %(self.customer,self.paid_fee)

    class Meta:
        verbose_name = "Payment缴费记录表"
        verbose_name_plural ="Payment缴费记录表"
class Role(models.Model):
    '''角色信息'''
    name = models.CharField(max_length=32,unique=True)
    menus = models.ManyToManyField("Menu",blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Role角色信息表"
        verbose_name_plural ="Role角色信息表"

class Menu(models.Model):
    '''菜单'''
    name = models.CharField(verbose_name='菜单名称', max_length=32)
    url_name = models.CharField(verbose_name='url名称', max_length=64)
    url_type_choices = ((0,'alias'),(1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    class Meta:
        verbose_name = "Menu菜单表"
        verbose_name_plural ="Menu菜单表"

    def __str__(self):
        return self.name
class Branch(models.Model):
    '''存储所有校区'''
    name = models.CharField(max_length=32,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Branch校区表"
        verbose_name_plural ="Branch校区表"



