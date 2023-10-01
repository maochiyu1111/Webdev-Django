"""
URL configuration for demo2 project.

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
from management import views

urlpatterns = [
    # 部门管理
    path("depart/list/", views.show_depart_list),
    path("depart/add/", views.add_depart),
    path("depart/delete/", views.delete_depart),
    path("depart/edit/", views.edit_depart),

    # 职工管理
    path("employee/list/", views.show_employee_list),
    path("employee/add/", views.add_employee),
    path("employee/edit/", views.edit_employee),
    path("employee/delete/", views.delete_employee),

]
