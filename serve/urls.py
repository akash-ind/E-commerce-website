from django.urls import path
from . import views

app_name="serve"
urlpatterns=[
	path("login",views.login_form,name="login"),
	path("show-table",views.show, name="show-table"),
	path("process", views.process, name="process"),
	path('prints',views.printing_process,name="provide-print"),
	path('download-prints/<int:id>',views.download_file,name="download-file"),
	path('download-config/<int:id>',views.download_info,name="download-config"),
	path('delete-file/<int:id>',views.deletefile,name="deletefile"),
	path('custom-order',views.process_custom_order,name="view-custom-order"),
	path('delivered-custom-order/<int:id>',views.delivered_custom_order, name='delivered'),
	path('logout',views.logout_user,name='logout'),
	path('delete/unprocessed',views.delete_unprocessed_prints,name="remove-unprocessed"),
	path('order/cancel',views.cancel_order,name="cancel-order"),
	path('order/cancel/custom',views.cancel_custom, name="cancel-custom"),
	path('order/expand',views.expand_order,name="expand-order"),
	path('order/custom/expand',views.expand_custom,name="expand-custom")
]