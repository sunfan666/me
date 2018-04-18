#coding:utf-8

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from dashboard.models import Department
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
# 引用方式 setting.TEMPLATE_JUMP


'''
class UserListView(TemplateView):
    template_name = 'user/userlist.html'
    before_index = 5
    after_index = 5

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        userlist = User.objects.all() #get all user list object.
        paginator = Paginator(userlist, 10) # 实例化Paginator
        page = self.request.GET.get('page', 1) #获取当前页码默认第一页
        try:
            page_obj = paginator.page(page) #获取当前页数据
        except EmptyPage:
            page_obj = paginator.page(1)
        context['page_obj'] = page_obj
        start_index = page_obj.number - self.before_index
        end_index = page_obj.number + self.after_index
        if start_index < 0:
            start_index = 0
        page_range = page_obj.paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


    def get(self, request, *args, **kwargs):
        self.request = request
        return super(UserListView, self).get(request, *args, **kwargs)
'''
class UserLISTVIEW(ListView):
    template_name = 'user/userlistl.html'
    model = User #指定数据去哪里找
    paginate_by = 10 #每页数据多少条
    before_index = 5
    after_index = 5

    def get_context_data(self, **kwargs):
        context = super(UserLISTVIEW, self).get_context_data(**kwargs)
        # page_obj = context['page_obj']
        # start_index = page_obj.number - self.before_index
        # end_index = page_obj.number + self.after_index
        # if start_index < 0:
        #     start_index = 0
        # page_range = page_obj.paginator.page_range[start_index:end_index]
        context['page_range'] = self.get_page_range(context['page_obj'])
        return context

    def get_page_range(self, page_obj):
        start_index = page_obj.number - self.before_index
        end_index = page_obj.number + self.after_index
        if start_index < 0:
            start_index = 0
        return page_obj.paginator.page_range[start_index:end_index]

class ModifyUserStatusView(View):
    def post(self, request):
        ret = {'status': 0}
        user_id = request.POST.get('user_id', None)
        print user_id
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户不存在'
        return JsonResponse(ret, safe=True)

class ModifyDepartmentView(TemplateView):
    template_name = 'user/modify_department.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyDepartmentView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['user_obj'] = get_object_or_404(User, pk=self.request.GET.get('user', None))
        return context

    #避免ajax方式更改数据,下边的get是为了防止猜测到URL是什么进而修改数据
    #只要是http请求，都加上权限验证,所以一定将权限控制到密不透风的地步，不要有任何漏洞。
    @method_decorator(login_required)
    @method_decorator(permission_required('dashboard.change_department', login_url=settings.PERMISSION_NONE_URL))
    def post(self, request):
        print request.POST
        user_id = request.POST.get('id', None)
        department_id = request.POST.get('department_id', None)
        if not user_id or not department_id:
            raise Http404
        try:
            user_obj = User.objects.get(pk=user_id)
            department_obj = Department.objects.get(pk=department_id)
        except:
            raise Http404
        else:
            user_obj.profile.department = department_obj
            user_obj.profile.save()
        return redirect('/user/userlist/')
    #在这里加上权限是因为如果没权限的话，界面虽然看不到'部门'了
    @method_decorator(login_required)
    @method_decorator(permission_required('dashboard.change_department', login_url=settings.PERMISSION_NONE_URL))
    def get(self, request, *args, **kwargs):
        self.request = request
        return super(ModifyDepartmentView, self).get(request, *args, **kwargs)

class ModifyPhoneView(TemplateView):
    template_name = 'user/modify_userinfo.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyPhoneView, self).get_context_data(**kwargs)
        uid = self.request.GET.get('uid')
        context['user_obj'] = self.get_user_obj(uid)
        return context

    def post(self, request):
        print request.POST
        uid = request.POST.get('id', None)
        user_obj = self.get_user_obj(uid)
        user_obj.profile.phone = request.POST.get('phone', None)
        user_obj.profile.cn_name = request.POST.get('cn_name', None)
        user_obj.profile.title = request.POST.get('title', None)
        user_obj.profile.save()
        return render(request, settings.TEMPLATE_JUMP, {"status": 0, "next_url":"/user/userlist"})
        # return redirect('/user/userlist/')

    def get_user_obj(self, uid):
        try:
            return  User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise Http404