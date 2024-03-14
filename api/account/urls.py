from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path("all/", UsersView.as_view(), name="list-users"),
    path("details/<user_id>/", UserDetailsView.as_view(), name="single-user"),
    path("login/", LoginUserView.as_view(), name="login-user"),
    path("register/", RegisterView.as_view(), name="register-user"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
