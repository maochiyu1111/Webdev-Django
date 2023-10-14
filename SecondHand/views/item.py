from django.shortcuts import render, HttpResponse, redirect


def show(request):
    return render(request, 'item_list.html')