from django.contrib import admin
from django.urls import path, include
from studentorg import views
# 1. ADD THIS SPECIFIC IMPORT
from allauth.account.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),

    # 2. ADD THIS LINE ABOVE THE ALLAUTH INCLUDE
    # This tells Django: "Go to the 'Account' folder, not the default 'account' folder"
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='account_login'),

    # 3. The rest of your routes
    path("accounts/", include("allauth.urls")),
    path('', views.HomePageView.as_view(), name='home'),

    # Organization List
    path('organization_list', views.OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', views.OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<int:pk>/', views.OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', views.OrganizationDeleteView.as_view(), name='organization-delete'),

    # Org Member
    path('orgmember_list', views.OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add', views.OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<int:pk>/', views.OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<pk>/delete', views.OrgMemberDeleteView.as_view(), name='orgmember-delete'),

    # Student
    path('student_list', views.StudentListView.as_view(), name='student-list'),
    path('student_list/add', views.StudentCreateView.as_view(), name='student-add'),
    path('student_list/<int:pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete', views.StudentDeleteView.as_view(), name='student-delete'),

    # College
    path('college_list', views.CollegeListView.as_view(), name='college-list'),
    path('college_list/add', views.CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>', views.CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete', views.CollegeDeleteView.as_view(), name='college-delete'),

    # Program
    path('program_list', views.ProgramListView.as_view(), name='program-list'),
    path('program_list/add', views.ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<pk>', views.ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete', views.ProgramDeleteView.as_view(), name='program-delete'),
]