from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from SecondHand import models
from SecondHand.utils.pagination import Pagination
from SecondHand.utils.form import ItemModelForm, ComplaintReplyModelForm


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


def show_complaint(request):
    form = ComplaintReplyModelForm()
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["order_id__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.ComplaintInfo.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset, 10)
    context = {
        "form": form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'admin_complaint_list.html', context)


@csrf_exempt
def reply_complaint(request):
    if request.method == 'GET':
        order_id = request.GET.get("order_id")
        row_dict = models.ComplaintInfo.objects.filter(order_id=order_id).values('complaint_category','complaint_reason').first()
        if not row_dict:
            return JsonResponse({"status": False, 'error': "数据不存在。"})

        result = {
            "status": True,
            "data": row_dict
        }
        return JsonResponse(result)

    else:
        reply = request.POST.get("reply")
        manager_id = request.session["info"]["id"]
        order_id = request.POST.get("order_id")
        # 新增回复到数据库
        models.HandlingOpinionInfo.objects.create(manager_id=manager_id, order_id=order_id, opinion=reply)

        # 修改order表中的complaint_status一项，变成已回复
        order_obj = models.OrderInfo.objects.filter(order_id=order_id).first()
        order_obj.complaint_status = 3
        order_obj.save()

        return JsonResponse({"status": True})
