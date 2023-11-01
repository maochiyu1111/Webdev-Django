from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        path_exclude = ["/login/", "/register/", "/index/"]
        path_user = ["/item/list/", "/item/detail/", "/order/list/", "/order/item/", "/item/shoppingcart/list/",
                     "/item/favorite/list/"]
        path_manager = ["/admin/item/manage/", "/admin/complaint/list/", "/admin/account/manage/"]
        if request.path_info in path_exclude:
            return

        # 如果访问用户端页面，则要求登录，且必须是用户的账号
        if request.path_info in path_user:
            info_dict = request.session.get("info")
            user_type = info_dict["type"]
            if not info_dict or user_type != 1:
                return redirect('/login/')
            return

        # 如果访问管理端页面，则要求登录，且必须是管理员的账号
        if request.path_info in path_manager:
            info_dict = request.session.get("info")
            user_type = info_dict["type"]
            if not info_dict or user_type != 2:
                return redirect('/login/')
            return
