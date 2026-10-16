from django.urls import path

from .views import RegisterView, LoginView, LogOutView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('profile/', ProfileView.as_view()),
]
