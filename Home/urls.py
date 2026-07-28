from django.urls import path
from Home import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('About', views.About, name="About"),
    path('FAQ', views.FAQ, name="FAQ"),
    path('Login', views.Login, name="Login"),
    path('Logout', views.Logout, name="Logout"),
    path('Sign_up', views.Sign_up, name="SignUp"),
    path('Forget_password', views.Forget_password, name="Forget_password"),
    path('Services', views.Services, name="Services"),
    path('Customer', views.Customer, name='Customer'),
    path('Checkout', views.Checkout, name='Checkout'),
    path('MockPayment', views.mock_payment, name='MockPayment'),
    path('MockPaymentProcess', views.mock_payment_process, name='MockPaymentProcess'),
    path('handlerequest', views.handlerequest, name="HandleRequest"),
    path('After_Login', views.After_Login, name="After_Login"),
    path('Vehicles', views.Vehicles, name="Vehicles"),
    path('My_Requests', views.My_Requests, name="My_Requests"),
]