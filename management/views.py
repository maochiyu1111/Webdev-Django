from django.shortcuts import render, redirect
from management import models
from django import forms


# Create your views here.
def show_depart_list(request):
    """展示部门列表"""

    depart_list = models.Department.objects.all()
    return render(request, "depart_list.html", {"depart_list": depart_list})


def add_depart(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, "depart_add.html")
    else:
        title = request.POST.get("title")

        # 保存到数据库
        models.Department.objects.create(title=title)

        # 重定向回部门列表
        return redirect("/depart/list/")


def delete_depart(request):
    """删除部门"""
    nid = request.GET.get("nid")

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/depart/list/")


def edit_depart(request):
    """修改部门"""
    nid = request.GET.get("nid")
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    else:
        # 获取用户提交的标题
        title = request.POST.get("title")

        # 根据ID找到数据库中的数据并进行更新
        models.Department.objects.filter(id=nid).update(title=title)

        # 重定向回部门列表
        return redirect("/depart/list/")


def show_employee_list(request):
    """展示员工列表"""
    employee_list = models.EmployeeInfo.objects.all()
    """
    # 用Python的语法获取数据，与html文件中Django模板语法略有不同
    for obj in queryset:
        print(obj.id, obj.name, obj.salary, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id  # 获取数据库中存储的那个字段值
        # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。
    """
    return render(request, "employee_list.html", {"employee_list": employee_list})


# ###################  使用ModelForm  ###################

class EmployeeModelForm(forms.ModelForm):
    # name = forms.CharField(min_length=3, label="姓名")

    class Meta:
        model = models.EmployeeInfo
        fields = ["name", "pwd", "age", 'salary', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def add_employee(request):
    """添加员工"""
    if request.method == 'GET':
        form = EmployeeModelForm()
        return render(request, "employee_add.html", {"form": form})
    else:
        form = EmployeeModelForm(data=request.POST)
        if form.is_valid():
            # 如果数据合法，保存到数据库
            # models.UserInfo.objects.create(..)原始方法复杂
            form.save()
            return redirect('/employee/list/')

        # 校验失败（在页面上显示错误信息）
        return render(request, 'employee_add.html', {"form": form})


def edit_employee(request):
    """修改员工信息"""
    nid = request.GET.get('nid')
    row_obj = models.EmployeeInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = EmployeeModelForm(instance=row_obj)
        return render(request, "employee_edit.html", {"form": form})
    else:
        form = EmployeeModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            # 如果数据合法，保存到数据库
            # models.UserInfo.objects.create(..)原始方法复杂
            form.save()
            return redirect('/employee/list/')

        # 校验失败（在页面上显示错误信息）
        return render(request, 'employee_add.html', {"form": form})


def delete_employee(request):
    """删除部门"""
    nid = request.GET.get("nid")
    # 删除
    models.EmployeeInfo.objects.filter(id=nid).delete()
    # 重定向回部门列表
    return redirect("/employee/list/")