from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    # path('users/actionUrl', RegisterView.as_view()),
    path('actionUrl',RegisterView.home),
    path(' ',RegisterView.home)
]
