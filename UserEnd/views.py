from django.shortcuts import render, HttpResponse, redirect
from UserEnd.models import UserInfo


# Create your views here.
def hello(request):
    return render(request, "index.html")


def show_user_list(request):
    user_list = UserInfo.objects.all()
    return render(request, "user_list.html", {"user_list": user_list})


def add_user(request):
    if request.method == "GET":
        return render(request, "add_user.html")
    else:
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        age = request.POST.get("age")

        # 添加到数据库
        UserInfo.objects.create(name=name, password=pwd, age=age)
        return redirect("/info/")
        # return HttpResponse("name:{}, pwd:{}, age:{}".format(name, pwd, age))


def delete_user(request):
     nid = request.GET.get('nid')
     UserInfo.objects.filter(id=nid).delete()
     return redirect("/info/")