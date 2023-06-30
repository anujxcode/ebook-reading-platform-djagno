from django.urls import path
from account import views

urlpatterns = [
    path('signup/',views.signup, name="signup"),
    path('signin/',views.signin, name="signin"),
    path('logout/',views.logout, name="logout"),
    path('changepassword/',views.changepassword, name="changepassword"),
    path('resetpassword/',views.resetpassword, name="resetpassword"),
    path('verfiyreset/',views.verfiyreset, name="verfiyreset"),
    path('setnewpass/',views.setnewpass, name="setnewpass"),
]
