from django.db import models


class FavoriteView(models.Model):
    favorite_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField(verbose_name="用户id")
    item_id = models.BigIntegerField(verbose_name="物品id")
    favorite_time = models.DateField(verbose_name='收藏时间', auto_now_add=True)
    item_name = models.CharField(verbose_name="物品名称", max_length=32)
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)
    item_img = models.CharField(verbose_name="物品图片", max_length=1024)

    class Meta:
        db_table = 'favorite_items_view'
        managed = False
