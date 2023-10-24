from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from SecondHand.utils.code import check_code
from SecondHand import models
from SecondHand.utils.bootstrap import BootStrapForm, BootStrapModelForm
from SecondHand.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        # 登录错误后密码保留
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    USERTYPE_CHOICES = (
        (1, '用户'),
        (2, '管理员'),
    )
    usertype = forms.ChoiceField(
        label="用户身份",
        # choices=USERTYPE_CHOICES,
        widget=forms.Select(choices=USERTYPE_CHOICES),
        choices=USERTYPE_CHOICES

    )

    # code = forms.CharField(
    #     label="验证码",
    #     widget=forms.TextInput,
    #     required=True
    # )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class RegisterModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.UserInfo
        fields = ["username", "password", "confirm_password", "usertype"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


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

        # 用户名和密码正确
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
