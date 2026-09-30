from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [

    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'submit/',
        views.submit_complaint,
        name='submit_complaint'
    ),

    path(
        'complaint/<str:complaint_id>/',
        views.complaint_detail,
        name='complaint_detail'
    ),

    path(
        'complaint/<str:complaint_id>/delete/',
        views.delete_complaint,
        name='delete_complaint'
    ),

    path(
        'admin-panel/',
        views.admin_complaint_list,
        name='admin_complaint_list'
    ),

    path(
        'admin-panel/<str:complaint_id>/update/',
        views.update_status,
        name='update_status'
    ),

    path(
        'admin-panel/<str:complaint_id>/delete/',
        views.admin_delete_complaint,
        name='admin_delete_complaint'
    ),
]