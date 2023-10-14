from django.shortcuts import render, HttpResponse, redirect


def show(request):
    return render(request, 'admin_list.html')