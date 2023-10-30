from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms

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


class ItemModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['item_img']

    class Meta:
        model = models.ItemInfo
        fields = ['item_name', 'item_category', 'purchase_time', 'item_condition', 'price', 'location',
                  'item_img', 'item_description']


class ComplaintModelForm(BootStrapModelForm):
    class Meta:
        model = models.ComplaintInfo
        fields = ['complaint_category', 'complaint_reason']


class ComplaintReplyModelForm(BootStrapModelForm):
    bootstrap_disabled_fields = ['complaint_category', 'complaint_reason']

    class Meta:
        model = models.ComplaintInfo
        fields = ['complaint_category', 'complaint_reason']


class OpinionModelForm(BootStrapModelForm):
    bootstrap_disabled_fields = ['manager', 'opinion']

    class Meta:
        model = models.HandlingOpinionInfo
        fields = ['manager', 'opinion']

