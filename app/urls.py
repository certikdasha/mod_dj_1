from django.urls import path
from .views import ProductListView, Login, Logout, Register, ProductCreateView, ProductDeleteView, ProductUpdateView, \
    ProductBuyView, OrderListView, RefundView, RefundListView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product-delete'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='product-update'),
    path('product/buy/<int:pk>', ProductBuyView.as_view(), name='product-buy'),
    path('my_orders/', OrderListView.as_view(), name='order-list'),
    path('refund/create/<int:pk>', RefundView.as_view(), name='refund-create'),
    path('refunds/', RefundListView.as_view(), name='refund'),
]
