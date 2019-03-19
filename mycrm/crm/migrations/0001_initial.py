# Generated by Django 2.1.7 on 2019-03-19 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('name', models.CharField(max_length=32, verbose_name='用户姓名')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Branch校区表',
                'verbose_name': 'Branch校区表',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.SmallIntegerField(choices=[(0, '面授(脱产)'), (1, '面授(周末)'), (2, '随到随学网络')], default=0, verbose_name='班级类型')),
                ('semester', models.PositiveSmallIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结业日期')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Branch', verbose_name='校区')),
            ],
            options={
                'verbose_name_plural': 'ClassList班级信息表',
                'verbose_name': 'ClassList班级信息表',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='课程名')),
                ('price', models.PositiveSmallIntegerField(verbose_name='课程价格')),
                ('outline', models.TextField(verbose_name='课程大纲')),
                ('period', models.IntegerField(verbose_name='课程周期(Month)')),
            ],
            options={
                'verbose_name_plural': 'Course课程信息表',
                'verbose_name': 'Course课程信息表',
            },
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='第几节课（天）')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework_title', models.CharField(blank=True, max_length=128, null=True, verbose_name='作业标题')),
                ('homework_content', models.TextField(blank=True, null=True, verbose_name='作业内容')),
                ('outline', models.TextField(verbose_name='本节课程大纲')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='上课日期')),
                ('from_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='班级')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师')),
            ],
            options={
                'verbose_name_plural': 'CourseRecord上课记录表',
                'verbose_name': 'CourseRecord上课记录表',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='姓名')),
                ('qq', models.CharField(help_text='QQ号必须唯一', max_length=64, unique=True, verbose_name='qq号')),
                ('qq_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='qq名称')),
                ('source', models.SmallIntegerField(choices=[(0, '转介绍'), (1, 'qq'), (2, '微信'), (3, '官方论坛'), (4, '网上搜索'), (5, '其他')], verbose_name='来源')),
                ('referral_from', models.CharField(blank=True, max_length=64, null=True, verbose_name='转介绍人qq')),
                ('content', models.TextField(verbose_name='咨询详情')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='咨询日期')),
                ('status', models.IntegerField(choices=[(0, '未报名'), (1, '已报名')], default=0, help_text='选择客户此时的状态', verbose_name='报名状态')),
                ('consult_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Course', verbose_name='咨询课程')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='课程顾问')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'Customer客户信息表',
                'verbose_name': 'Customer客户信息表',
            },
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='跟进内容')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='跟进日期')),
                ('status', models.IntegerField(choices=[(1, '近期无报名计划'), (2, '2个月内报名'), (3, '1个月内报名'), (4, '2周内报名'), (5, '1周内报名'), (6, '2天内报名'), (7, '已报名'), (8, '已交全款')], help_text='选择客户此时的状态', verbose_name='状态')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='跟踪人')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='所咨询客户')),
            ],
            options={
                'verbose_name_plural': 'CustomerFollowUp客户跟进表',
                'verbose_name': 'CustomerFollowUp客户跟进表',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_agreed', models.BooleanField(verbose_name='学员已同意合同')),
                ('contract_approved', models.BooleanField(help_text='合同已审核', verbose_name='审批通过')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='课程顾问')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer')),
                ('enrolled_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='所报班级')),
            ],
            options={
                'verbose_name_plural': 'Enrollment学员报名表',
                'verbose_name': 'Enrollment学员报名表',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('url_name', models.CharField(max_length=64, verbose_name='url名称')),
                ('url_type', models.SmallIntegerField(choices=[(0, 'alias'), (1, 'absolute_url')], default=0)),
            ],
            options={
                'verbose_name_plural': 'Menu菜单表',
                'verbose_name': 'Menu菜单表',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_fee', models.IntegerField(default=0, verbose_name='费用数额')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='交款日期')),
                ('consultant', models.ForeignKey(help_text='谁签的单就选谁', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='负责老师')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer')),
            ],
            options={
                'verbose_name_plural': 'Payment缴费记录表',
                'verbose_name': 'Payment缴费记录表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('menus', models.ManyToManyField(blank=True, to='crm.Menu')),
            ],
            options={
                'verbose_name_plural': 'Role角色信息表',
                'verbose_name': 'Role角色信息表',
            },
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(choices=[(0, '已签到'), (1, '迟到'), (2, '缺勤'), (3, '早退')], default='checked', max_length=64, verbose_name='上课纪录')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (-50, 'D'), (0, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=0, verbose_name='本节成绩')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.CourseRecord', verbose_name='第几天课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='学员')),
            ],
            options={
                'verbose_name_plural': 'StudyRecord学习成绩表',
                'verbose_name': 'StudyRecord学习成绩表',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Tag标签',
                'verbose_name': 'Tag标签',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, to='crm.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Course', verbose_name='课程'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='studyrecord',
            unique_together={('course_record', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('customer', 'enrolled_class')},
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together={('from_class', 'day_num')},
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together={('branch', 'course', 'semester')},
        ),
    ]
