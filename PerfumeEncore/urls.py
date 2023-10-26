"""
URL configuration for PerfumeEncore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SecondHand.views import account, item, admin, order
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [

    # 主页
    path('index/', account.index),

    # 图片上传
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    # path('image/code/', account.image_code),
    path('register/', account.register),

    # 物品展示
    path('item/list/', item.show_list),
    path('item/add/', item.add),
    path('item/detail/', item.show_detail),

    # 订单部分
    path('order/add/', order.add),
    path('order/list/', order.show_list),
    path('order/item/', order.check_item),
    path('order/delete/', order.delete),
    path('order/complaint/', order.add_complaint),
    path('order/check/reply/', order.check_reply),

    # 管理员视角
    path('admin/item/manage/', admin.show_item),
    path('admin/item/detail/', admin.check_item),
    path('admin/item/delete/', admin.delete_item),
    path('admin/complaint/list/', admin.show_complaint),
    path('admin/complaint/reply/', admin.reply_complaint),




]