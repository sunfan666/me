#coding:utf-8

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission, ContentType
from dashboard.models import Department
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.conf import settings
import logging
logger = logging.getLogger('opsweb')

class GroupListView(ListView):
    model = Group
    template_name = 'user/grouplist.html'

    def post(self, request):
        ret = {'status': 0}
        name = request.POST.get('name', '')
        if name:
            try:
                group = Group()
                group.name = name
                group.save()
            except Exception as e:
                ret['status'] = 1
                ret['errmsg'] = e.args
        return JsonResponse(ret, safe=True)

class GroupView(View):
    """
    获取所有用户组信息
    """
    def get(self,request):
        uid = request.GET.get('uid')
        ret = {'status': 0}
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户不存在'
        all_groups = Group.objects.all()
        user_groups = user.groups.all()
        groups = [group for group in all_groups if group not in user_groups]

        return HttpResponse(serializers.serialize('json', groups), content_type='application/json')

class GroupdelView(View):
    """
    获取本用户所在用户组信息
    """
    def get(self,request):
        uid = request.GET.get('uid')
        ret = {'status': 0}
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户不存在'
        all_groups = Group.objects.all()
        user_groups = user.groups.all()
        groups = [group for group in all_groups if group in user_groups]

        return HttpResponse(serializers.serialize('json', groups), content_type='application/json')

class UserGroupView(View):
    """
    取出用户组内的用户信息
    """
    def get(self, request):
        gid = request.GET.get('gid', None)
        try:
            group = Group.objects.get(pk=gid)
        except:
            return JsonResponse([], safe=False)
        users = group.user_set.all()
        user_list = [{"username":user.username, "email":user.email, "cn_name":user.profile.cn_name, "id":user.id} for user in users]
        return JsonResponse(user_list, safe=False)

    """
    将用户添加到指定组
    """
    def post(self, request):
        ret = {'status': 0}
        print request.POST
        uid = request.POST.get('uid', None)
        gid = request.POST.get('gid', None)

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            logger.error('将用户添加到指定组，用户不存在，用户ID为%s' % uid)
            ret['status'] =1
            ret['errmsg'] = '用户不存在'
            return JsonResponse(ret, safe=True)

        try:
            group = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            logger.error('将用户添加到指定组，用户组不存在，用户组ID为%s' % gid)
            ret['status'] = 2
            ret['errmsg'] = '用户组不存在'
            return JsonResponse(ret, safe=True)
        user.groups.add(group)
        return JsonResponse(ret, safe=True)

    """
    将用户从组内删除
    """
    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        uid = data.get('userid', None)
        gid = data.get('groupid', None)
        try:
            user = User.objects.get(pk=uid)
            group = Group.objects.get(pk=gid)
            group.user_set.remove(user)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户不存在'
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户组不存在'
        except Exception as e:
            ret['status'] = 1
            ret['errmsg'] = e.args
        return JsonResponse(ret, safe=True)

class RemoveUserGroupView(View):
    """
    将指定组从用户所属组中删除
    """
    def post(self, request):
        ret = {'status': 0}
        uid = request.POST.get('uid', None)
        gid = request.POST.get('gid', None)

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            logger.error('将用户从指定组删除，用户不存在，用户ID为%s' % uid)
            ret['status'] =1
            ret['errmsg'] = '用户不存在'
            return JsonResponse(ret, safe=True)

        try:
            group = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            logger.error('将用户从指定指定组删除，用户组不存在，用户组ID为%s' % gid)
            ret['status'] = 2
            ret['errmsg'] = '用户组不存在'
            return JsonResponse(ret, safe=True)
        user.groups.remove(group)
        return JsonResponse(ret, safe=True)


class GroupPermissionListView(TemplateView):
    template_name = 'user/group_permission_list.html'
    """
    修改用户组权限
    """
    def get_context_data(self, **kwargs):
        context = super(GroupPermissionListView, self).get_context_data(**kwargs)
        context['group'] = self.request.GET.get('gid', None)
        context['group_permissions'] = self.get_group_permissions()
        context['content_type'] = ContentType.objects.all()
        return context

    def get_group_permissions(self):
        gid = self.request.GET.get('gid', None)
        try:
            group = Group.objects.get(pk=gid)
            return [per.id for per in group.permissions.all()]
        except Group.DoesNotExist:
            raise Http404

    def post(self, request):
        print request.POST
        ret = {"status": 0, "next_url": "/group/list"}
        permission_id_list = request.POST.getlist('permission', []) #获取出权限列表
        groupid = request.POST.get('group', None) #取出用户组ID
        try:
            group = Group.objects.get(pk=groupid) #取出这个用户组对象
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户组不存在'
        else:
            if permission_id_list:
                permission_obj = Permission.objects.filter(id__in=permission_id_list)
                group.permissions = permission_obj #给用户组赋权限值
        return render(request, settings.TEMPLATE_JUMP, ret)

# class GroupPermissionView(ListView):
#     template_name = 'user/group_permission.html'
#     model = Permission
#     context_object_name = 'object_list'
#
#     def get_queryset(self):
#         queryset = super(GroupPermissionView, self).get_queryset()
#         gid = self.request.GET.get('gid', 0)
#         try:
#             group = Group.objects.get(pk=gid)
#             permission = group.permissions.all()
#         except Group.DoesNotExist:
#             raise Http404
#         queryset = queryset.filter(id__in=[p.id for p in permission])#模型查出来的数据做过滤可以用queryset
#         return queryset

'''
上边的类函数（GroupPermissionView）也可以使用template模版，更简单。
'''
class GroupPermissionView(TemplateView):
    template_name = 'user/group_permission.html'

    def get_context_data(self, **kwargs):
        context_data = super(GroupPermissionView, self).get_context_data(**kwargs)
        gid = self.request.GET.get('gid', 0)
        try:
            group = Group.objects.get(pk=gid)
            context_data['permissions'] = group.permissions.all()
        except Group.DoesNotExist:
            raise Http404
        return context_data