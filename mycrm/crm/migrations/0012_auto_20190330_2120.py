# Generated by Django 2.1.7 on 2019-03-30 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_payment_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyrecord',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Enrollment', verbose_name='学员'),
        ),
    ]
