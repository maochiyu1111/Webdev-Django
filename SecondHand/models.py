from django.db import models


class UserInfo(models.Model):
    """ 用户表"""
    username = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    create_time = models.DateField(verbose_name="创建时间", auto_now_add=True)

    usertype_choices = (
        (1, "用户"),
        (2, "管理员"),
    )
    usertype = models.SmallIntegerField(verbose_name="用户身份", choices=usertype_choices)

    status_choices = (
        (1, "注销"),
        (2, "正常"),
        (3, "冻结"),
    )
    statustype = models.SmallIntegerField(verbose_name="用户状态", choices=status_choices, default=2)


class ItemInfo(models.Model):
    """ 二手物品表"""
    item_name = models.CharField(verbose_name="物品名称", max_length=32)
    item_category = models.ForeignKey(to="ItemCategory", to_field="id", on_delete=models.CASCADE)
    purchase_time = models.DateField(verbose_name="购买时间")

    condition_choices = (
        (1, "九成新"),
        (2, "七成新"),
        (3, "五成新"),
        (4, "其他"),
    )

    item_condition = models.SmallIntegerField(verbose_name="新旧程度", choices=condition_choices)

    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)

    location = models.CharField(verbose_name="交易位置", max_length=32)

    publish_time = models.DateField(verbose_name='发布时间', auto_now_add=True)


class ItemCategory(models.Model):
    """ 物品种类"""
    category_name = models.CharField(verbose_name="种类名称", max_length=32)