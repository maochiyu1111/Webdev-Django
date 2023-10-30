from django.shortcuts import render, HttpResponse, redirect
from SecondHand import models
from SecondHand.utils.form import LoginForm, RegisterModelForm


def index(request):
    return render(request, 'index.html')


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
        # return render(request, 'layout_user.html')

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 去数据库校验用户名和密码是否正确
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 再查看是否是被冻结的账户
        if user_object.statustype == 3:
            form.add_error("username", "您的账号已被冻结")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确且经过验证
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'name': user_object.username, 'type': user_object.usertype}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        if user_object.usertype == 1:
            return redirect("/item/list/")

        return redirect("/admin/item/manage/")

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        user_object = models.UserInfo.objects.filter(username=form.instance.username).first()
        if user_object:
            form.add_error("username", "用户名已存在")
            return render(request, 'register.html', {'form': form})

        form.save()
        return redirect('/login/')

    return render(request, 'register.html', {'form': form})


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')
