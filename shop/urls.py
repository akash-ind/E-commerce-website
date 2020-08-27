from django.urls import path
from . import views

app_name="shop"
urlpatterns=[
	path("",views.category,name="show"),
	path("<uuid:id>/",views.product,name="product"),
	path("cart/add/",views.add_to_cart,name="add-in-cart"),
	path("cart/remove",views.remove_from_cart,name="removing-from-cart"),
	path("cart/checkout",views.checkout,name="checkout"),
	path("cart/show",views.show_cart,name="show-cart"),
	path("product/specific-product",views.make_product,name="new_product"),
	path("<slug:category>/",views.specific_category,name="category_products"),
	path('order/cancel',views.cancel_order,name="cancel-order")
] 