from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from SecondHand import models
from SecondHand.utils.pagination import Pagination
from SecondHand.views.item import ItemModelForm


def show_item(request):
    form = ItemModelForm()
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["item_name__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.ItemInfo.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset, 10)
    context = {
        "form": form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'admin_item_list.html', context)


def delete_item(request):
    itemid = request.GET.get('itemid')
    exists = models.ItemInfo.objects.filter(id=itemid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    models.ItemInfo.objects.filter(id=itemid).delete()
    return JsonResponse({"status": True})


def check_item(request):
    itemid = request.GET.get("itemid")
    row_dict = models.ItemInfo.objects.filter(id=itemid).values('item_name', 'item_category', 'purchase_time',
                                                                'item_condition', 'price', 'location', 'item_description').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)