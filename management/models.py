from django.db import models


# Create your models here.
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title



class EmployeeInfo(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=32)
    pwd = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    salary = models.DecimalField(verbose_name='薪水', max_digits=10, decimal_places=2, default=1000)
    create_time = models.DateField(verbose_name='入职时间')

    # 外键约束与级联
    # Django会在数据库生成depart_id一列
    depart = models.ForeignKey(verbose_name='部门', to="Department", to_field="id", on_delete=models.CASCADE)
    # 如果不想级联删除，可以置空
    # depart = models.ForeignKey(to="Department", to_field="id",
    # null=True, blank=True, on_delete=models.SET_NULL)

    # 定类变量可以在django中做如下约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)