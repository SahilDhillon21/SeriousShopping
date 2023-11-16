from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('addReview/',views.addReview,name='addReview'),
	path('deleteReview/<review_id>',views.deleteReview,name='deleteReview'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('view_product/<prodID>', views.viewProduct, name="view_product"),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('become-a-seller/',views.create_seller,name='become-a-seller'),
    path('seller-dashboard/',views.seller_dashboard,name='seller-dashboard'),
    path('add-product/',views.addProduct,name='add-product'),
    path('remove-product/<productID>',views.removeProduct,name='remove-product'),
]