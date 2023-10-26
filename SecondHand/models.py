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

    def __str__(self):
        return self.username


class ItemInfo(models.Model):
    """ 二手物品表"""

    seller = models.ForeignKey(verbose_name="卖家ID", to="UserInfo", to_field="id", on_delete=models.CASCADE)
    item_name = models.CharField(verbose_name="物品名称", max_length=32)
    item_category = models.ForeignKey(verbose_name="物品种类", to="ItemCategory", to_field="id",
                                      on_delete=models.CASCADE)
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

    item_img = models.FileField(verbose_name="物品图片", max_length=1024, upload_to='item/')

    item_description = models.TextField(verbose_name='物品描述', max_length=512, blank=True)


class ItemCategory(models.Model):
    """ 物品种类"""
    category_name = models.CharField(verbose_name="种类名称", max_length=32)

    def __str__(self):
        return self.category_name


class OrderInfo(models.Model):
    # item_id in database
    item = models.ForeignKey(verbose_name="物品id", to="ItemInfo", to_field="id", on_delete=models.CASCADE)

    item_name = models.CharField(verbose_name="物品名称", max_length=32)

    buyer = models.ForeignKey(verbose_name="买方id", to="UserInfo", to_field="id", on_delete=models.CASCADE)

    amount = models.DecimalField(verbose_name='交易价格', max_digits=10, decimal_places=2)

    order_time = models.DateField(verbose_name='支付时间', auto_now_add=True)

    order_status_choices = (
        (1, "未完成"),
        (2, "已完成"),
        (3, "已取消"),
    )

    order_status = models.SmallIntegerField(verbose_name="订单状态", choices=order_status_choices)

    order_complaint_choices = (
        (1, "未发起投诉"),
        (2, "已投诉，未回复"),
        (3, "已投诉，且回复"),
    )

    order_complaint_status = models.SmallIntegerField(verbose_name="订单投诉状态", choices=order_complaint_choices,
                                                      default=1)


class FavoriteInfo(models.Model):
    user = models.ForeignKey(verbose_name="用户id", to="UserInfo", to_field="id", on_delete=models.CASCADE)

    item = models.ForeignKey(verbose_name="物品id", to="ItemInfo", to_field="id", on_delete=models.CASCADE)

    favorite_time = models.DateField(verbose_name='收藏时间', auto_now_add=True)


class ShoppingCartInfo(models.Model):
    user = models.ForeignKey(verbose_name="用户id", to="UserInfo", to_field="id", on_delete=models.CASCADE)

    item = models.ForeignKey(verbose_name="物品id", to="ItemInfo", to_field="id", on_delete=models.CASCADE)

    add_time = models.DateField(verbose_name='加购时间', auto_now_add=True)


class ComplaintInfo(models.Model):
    user = models.ForeignKey(verbose_name="用户id", to="UserInfo", to_field="id", on_delete=models.CASCADE)

    order = models.OneToOneField(verbose_name="订单id", to="OrderInfo", to_field="id",
                                 on_delete=models.CASCADE, primary_key=True)

    category_choices = (
        (1, "对卖家"),
        (2, "对物品"),
    )

    complaint_category = models.SmallIntegerField(verbose_name="投诉类别", choices=category_choices)

    complaint_time = models.DateField(verbose_name='投诉时间', auto_now_add=True)

    complaint_reason = models.TextField(verbose_name='投诉理由', max_length=512)



class HandlingOpinionInfo(models.Model):
    order = models.OneToOneField(verbose_name="订单id", to="OrderInfo", to_field="id",
                                 on_delete=models.CASCADE, primary_key=True)

    manager = models.ForeignKey(verbose_name="管理员", to="UserInfo", to_field="id", on_delete=models.CASCADE)

    opinion = models.TextField(verbose_name='处理意见', max_length=512)

    handling_time = models.DateField(verbose_name='处理时间', auto_now_add=True)

