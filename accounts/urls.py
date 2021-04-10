from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:user_id>/', views.UserPage , name ="user-page"),
    path('store/' , views.userStore , name='user-store'),    

    path('', views.home , name="home" ),
    path('customer/<str:customer_id>' , views.customer , name="customer" ),
    

    path('create_tag/' , views.createTag , name="create_tag" ),

    path('products/' , views.products , name="products" ),
    path('create_product/' , views.createProduct , name="create_product" ),
    path('delete_product/<str:product_id>' , views.deleteProduct , name="delete_product" ),
    path('update_product/<str:product_id>' , views.updateProduct , name="update_product" ),

    path('create_order/<str:customer_id>/' , views.createOrder , name='create_order')	,
    path('update_order/<str:order_id>' , views.UpdateOrder , name='update_order')	,
    path('delete_order/<str:order_id>' , views.DeleteOrder , name='delete_order')	,
    
    path('login/' , views.UserLogin , name='login'),
    path('logout/' , views.UserLogout , name='logout'),
    path('register/' , views.UserRegister , name='register'),
]
	