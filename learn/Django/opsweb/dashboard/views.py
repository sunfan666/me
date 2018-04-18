#coding: utf-8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import logging

logger = logging.getLogger('opsweb')



def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html', {"title":"必优云运营平台"})
    elif request.method == 'POST':
        ret = {"status":0}
        ret["errmsg"] = '登陆成功'
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        #验证用户密码
        user = authenticate(username=username, password=password)
        print user
        # 如果用户名密码不存在/用户名不存在/密码不对 这些情况都会返回None
        if user is not None:
            if user.is_active:
                #  将用户信息写入session 将session_key写入cookie
                login(request, user)
                ret["next_url"] = '/'
            else:
                ret["status"] = 1
                ret["errmsg"] = '用户被禁用'
        else:
            ret["status"] = 2
            ret["errmsg"] = '用户名或密码错误'
        return JsonResponse(ret, safe=True)
    return JsonResponse(ret, safe=True)

@login_required
def user_logout(request):
    # 这一步会把session的值置为空，key不删除
    logout(request)
    return HttpResponseRedirect('/login')

class IndexView(View):
    @method_decorator(login_required)#哪个页面需要登录才能显示页面内容就加这个装饰器即可
    # @method_decorator(permission_required('dashboard.view_server', login_url=settings.PERMISSION_NONE_URL))
    def get(self, request):   #必须是method种的方法URL种的as_view()就是找类中的请求方法函数,比如get post put
        logger.error('首页error测试')
        logger.debug('首页debug测试')

        return render(request, "public/index.html")


def test_form(request):
    if request.method == 'GET':
        return render(request, 'test/test_form.html')
    elif request.method == 'POST':
        # print request.POST
        # print request.POST.lists()
        # print request.POST.dict()
        # username = request.POST.get('username', '')
        # print username
        # # fav = request.POST.get('fav')
        # #要写上第二个参数 默认值是什么 习惯问题
        # fav = request.POST.getlist('fav', [])
        # print fav
        #form表单提交的数据都写在body体里边（无论哪种方式提交）
        print request.body
        return HttpResponse('ok')
    #如果除了get&post之外的请求方式，取值方式如下：
    # else:
    #     data = QueryDict(request.body)
    #     fav = data.get('fav[]','')
    #     print fav
    #     fav2 = data.getlist('fav[]','')
    #     print fav2
    
@login_required
def permission(request):
    return render(request, 'public/permission.html')