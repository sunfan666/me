#!/usr/bin/env python
#coding: utf-8
from django.conf.urls import include,url
from . import views
from . import user
from dashboard.user import group
from . import cmdb

urlpatterns=[
 url(r'^login/$',views.user_login),
 url(r'^logout/$',views.user_logout),
 url(r'^$',views.IndexView.as_view()),#as_view()去找类视图中的http－requets－method


 url(r'^user/', include([
    url(r'^userlist/$', user.UserLISTVIEW.as_view()),
    url(r'^modifystatus/$', user.ModifyUserStatusView.as_view()),
    url(r'^modifydepartment/$', user.ModifyDepartmentView.as_view()),
    url(r'^modifyphone/$', user.ModifyPhoneView.as_view()),
 ])),


 url(r'^permission/', include([
    url(r'^none/$', views.permission),
 ])),



 url(r'^group/', include([
    url(r'^$', group.GroupView.as_view()),
    url(r'^del/$', group.GroupdelView.as_view()),
    url(r'^list/$', group.GroupListView.as_view()),
    url(r'^usergroup/$', group.UserGroupView.as_view()),
    url(r'^delgroup/$', group.RemoveUserGroupView.as_view()),
    url(r'^permissionlist/$', group.GroupPermissionListView.as_view()),
    url(r'^permissions/$', group.GroupPermissionView.as_view()),
 ])),


 url(r'^cmdb/', include([
    url(r'^idclist/$', cmdb.ServerView),
 ])),
]

