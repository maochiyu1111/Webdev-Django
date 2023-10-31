from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from SecondHand import models
from SecondHand.utils.form import ComplaintModelForm, OpinionModelForm


def add(request):
    item_id = request.GET.get('item_id')
    amount = request.GET.get('amount')
    item_name = request.GET.get('item_name')
    buyer_id = request.session["info"]["id"]
    if item_id:
        models.OrderInfo.objects.create(item_id=item_id, buyer_id=buyer_id, amount=amount, order_status=1,
                                        item_name=item_name)
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


def show_list(request):
    buyer_id = request.session["info"]["id"]
    order_list = models.OrderInfo.objects.filter(buyer_id=buyer_id)
    complaint_form = ComplaintModelForm()
    opinion_form = OpinionModelForm()
    context = {
        "complaint_form": complaint_form,
        "order_list": order_list,
        "opinion_form": opinion_form
    }

    return render(request, 'order_list.html', context)


def check_item(request):
    item_id = request.GET.get('itemid')
    item_object = models.ItemInfo.objects.filter(id=item_id).first()
    return render(request, 'order_item.html', {"item_object": item_object})


def delete(request):
    order_id = request.GET.get('orderid')
    exists = models.OrderInfo.objects.filter(id=order_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "取消失败，订单不存在。"})

    models.OrderInfo.objects.filter(id=order_id).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def add_complaint(request):
    order_id = request.POST.get('order_id')
    exists = models.ComplaintInfo.objects.filter(order_id=order_id).exists()
    if exists:
        return JsonResponse({"status": False, 'error': "你已投诉过该订单，请勿重复投诉"})

    form = ComplaintModelForm(data=request.POST)
    if form.is_valid():
        complaint_reason = form.instance.complaint_reason
        complaint_category = form.instance.complaint_category
        order_id = request.POST.get('order_id')
        user_id = request.session["info"]["id"]
        models.ComplaintInfo.objects.create(user_id=user_id, order_id=order_id, complaint_reason=complaint_reason,
                                            complaint_category=complaint_category)

        # 修改order表中的complaint_status一项
        order_obj = models.OrderInfo.objects.filter(id=order_id).first()
        order_obj.order_complaint_status = 2
        order_obj.save()

        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': "未按要求填写"})


def check_reply(request):
    order_id = request.GET.get("order_id")
    row_dict = models.HandlingOpinionInfo.objects.filter(order_id=order_id).values('manager',
                                                                                   'opinion', 'handling_time').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "发生错误，数据不存在"})

    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)

