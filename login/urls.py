from django.urls import path
from . import views

app_name="login"
urlpatterns = [
	path("",views.home,name="home"),
	path("login/",views.login,name="login"),
	path("logout/",views.logout,name="logout"),
	path("register/",views.register_user,name="register"),
	path("verify/",views.mail,name="verify_user"),
	path("reset-password/",views.reset,name="reset"),
	path("change-password/<uuid:id>",views.verify,name="verify_for_time"),
	path("change-pass/<uuid:id>",views.change_password,name="change_pass"),
	path("user/add-address/",views.add_address,name="add_address"),
	path("review/<uuid:id>/",views.review,name="review_product"),
	path("cancel/<uuid:id>/",views.cancel,name="cancel_product"),
	path("user/profile/",views.account,name="view_profile"),
]
	
