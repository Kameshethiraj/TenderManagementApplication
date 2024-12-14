from django.urls import path
from .views import LoginView, BiddingAddView, ListBiddingView, UpdateBiddingView, DeleteBiddingView, RegistrationView, LogoutView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='Register' ),
    path('login/', LoginView.as_view(), name='login'),
    path('bidding/add/', BiddingAddView.as_view(), name='add_bidding'),
    path('bidding/list/', ListBiddingView.as_view(), name='list_bidding'),
    path('bidding/update/<int:pk>/', UpdateBiddingView.as_view(), name='update_bidding'),
    path('bidding/delete/<int:pk>/', DeleteBiddingView.as_view(), name='delete_bidding'),
    path('logout/', LogoutView.as_view(), name='logout')
]
# AddBiddingView, ListBiddingView, UpdateBiddingView, DeleteBiddingView
# http://127.0.0.1:8000/bidding/list/?bidAmount=1300000