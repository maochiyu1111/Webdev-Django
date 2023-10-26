from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from SecondHand import models
from SecondHand.utils.pagination import Pagination
from SecondHand.utils.form import ItemModelForm


def show_list(request):
    form = ItemModelForm()
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["item_name__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.ItemInfo.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset, 3)
    context = {
        "form": form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'item_list.html', context)


@csrf_exempt
def add(request):
    """ 新建物品（Ajax请求）"""
    form = ItemModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 固定设置卖家
        form.instance.seller_id = request.session["info"]["id"]

        # 保存到数据库中
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def show_detail(request):
    """ 物品详情"""
    itemid = request.GET.get('itemid')
    item_object = models.ItemInfo.objects.filter(id=itemid).first()
    return render(request, 'item_detail.html', {"item_object": item_object})
