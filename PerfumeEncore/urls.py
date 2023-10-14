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
from SecondHand.views import account, item, admin

urlpatterns = [
    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    # path('image/code/', account.image_code),
    path('register/', account.register),

    # 物品展示
    path('item/list/', item.show),
    # path('item/add/', item.add),

    # 管理员视角
    path('admin/list/', admin.show)

]