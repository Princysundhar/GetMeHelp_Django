"""django_getme_help URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.log),
    path('login_post',views.login_post),
    path('admin_home',views.admin_home),
    path('worker_home',views.worker_home),
    path('user_home',views.user_home),
    path('admin_view_registered_worker', views.admin_view_registered_worker),
    path('admin_registered_worker_approve/<log_id>',views.admin_registered_worker_approve),
    path('admin_registered_worker_reject/<log_id>',views.admin_registered_worker_reject),
    path('admin_view_approved_worker',views.admin_view_approved_worker),
    path('admin_block_worker/<log_id>',views.admin_block_worker),
    path('admin_unblock_worker/<log_id>',views.admin_unblock_worker),
    path('admin_view_rejected_worker',views.admin_view_rejected_worker),
    path('admin_view_registered_user',views.admin_view_registered_user),
    path('admin_view_compliant',views.admin_view_compliant),
    path('admin_send_reply/<repid>',views.admin_send_reply),
    path('admin_send_reply_post/<repid>',views.admin_send_reply_post),
    path('admin_view_rating_review',views.admin_view_rating_review),
    path('admin_change_password',views.admin_change_password),
    path('admin_change_password_post',views.admin_change_password_post),
    path('admin_add_category',views.admin_add_category),
    path('admin_add_category_post',views.admin_add_category_post),
    path('admin_category_view',views.admin_category_view),
    path('admin_category_delete/<i>',views.admin_category_delete),
    path('admin_category_update/<i>',views.admin_category_update),
    path('admin_category_update_post/<i>',views.admin_category_update_post),

 ##########################################################################################

    path('worker_register',views.worker_register),
    path('worker_register_post',views.worker_register_post),
    path('worker_view_profile',views.worker_view_profile),
    path('worker_edit_profile/<worker_id>',views.worker_edit_profile),
    path('worker_edit_profile_post/<worker_id>',views.worker_edit_profile_post),
    path('worker_add_service',views.worker_add_service),
    path('worker_add_service_post',views.worker_add_service_post),
    path('worker_service_view',views.worker_service_view),
    path('worker_service_delete/<service_id>',views.worker_service_delete),
    path('worker_service_update/<service_id>',views.worker_service_update),
    path('worker_service_update_post/<service_id>',views.worker_service_update_post),
    path('worker_view_request_from_user',views.worker_view_request_from_user),
    path('worker_status_approve/<rid>',views.worker_status_approve),
    path('worker_status_reject/<rid>',views.worker_status_reject),
    path('worker_add_additional_charges/<bid>',views.worker_add_additional_charges),
    path('worker_additional_charge_post/<bid>',views.worker_additional_charge_post),
    path('worker_view_payment',views.worker_view_payment),
    path('worker_view_rating_review',views.worker_view_rating_review),
    path('worker_change_password',views.worker_change_password),
    path('worker_change_password_post',views.worker_change_password_post),
    path('list_user_chat', views.list_user_chat),
    path('worker_chat_customer/<i>',views.worker_chat_customer),
    path('worker_chat_customer_post/<i>',views.worker_chat_customer_post),
    path('worker_add_bank',views.worker_add_bank),
    path('worker_add_bank_post',views.worker_add_bank_post),
    path('worker_view_bank', views.worker_view_bank),
    path('worker_delete_bank/<bid>',views.worker_delete_bank),
    path('worker_view_credit_point',views.worker_view_credit_point),
    path('worker_credit_convert/<cid>',views.worker_credit_convert),

###################################################################################################

    path('user_register',views.user_register),
    path('user_register_post',views.user_register_post),
    path('user_view_category',views.user_view_category),
    # path('user_view_workers/<wid>',views.user_view_workers),
    path('user_approved_worker/<wid>',views.user_approved_worker),
    path('user_view_service/<id>',views.user_view_service),
    path('user_view_request',views.user_view_request),
    path('user_booking_map/<rid>/<amount>',views.user_booking_map),
    path('user_send_request/<rid>/<amount>',views.user_send_request),
    path('user_view_bill/<bid>',views.user_view_bill),
    path('user_add_rating/<rid>',views.user_add_rating),
    path('user_add_rate_post/<rid>',views.user_add_rate_post),
    path('user_view_rating/<rid>',views.user_view_rating),
    path('list_worker_chat',views.list_worker_chat),
    path('user_chat_worker/<i>',views.user_chat_worker),
    path('user_chat_worker_post/<i>',views.user_chat_worker_post),
    path('user_send_complaint',views.user_send_complaint),
    path('user_send_complaint_post',views.user_send_complaint_post),
    path('user_view_reply',views.user_view_reply),
    path('user_change_password',views.user_change_password),
    path('user_change_password_post',views.user_change_password_post),
    path('user_add_bank',views.user_add_bank),
    path('user_add_bank_post',views.user_add_bank_post),
    path('user_view_bank',views.user_view_bank),
    path('user_delete_bank/<bid>',views.user_delete_bank),
    path('user_make_payment/<rid>',views.user_make_payment),
    path('user_make_payment_post/<rid>',views.user_make_payment_post),
    path('user_bank_details/<rid>/<wid>/<amount>',views.user_bank_details),
    path('user_bank_details_post/<rid>/<wid>/<amount>',views.user_bank_details_post),
    path('user_view_credit_point',views.user_view_credit_point),
    path('ajax_view_credit_points',views.ajax_view_credit_points),
    path('credit_payment_mode',views.credit_payment_mode),
]
