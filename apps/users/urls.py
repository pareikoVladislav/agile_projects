from django.urls import path

from apps.users.views import (
    UserListGenericView,
    RegisterUserGenericView,
    UserDetailView
)

urlpatterns = [
    path('', UserListGenericView.as_view()),
    path('register/', RegisterUserGenericView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
]
