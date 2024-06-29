from django.urls import path

from apps.users.views import UserListGenericView, RegisterUserGenericView
from tests.test_get_some_user_info import GetCurrentUserAPIView

urlpatterns = [
    path('', UserListGenericView.as_view()),
    path('register/', RegisterUserGenericView.as_view()),
    path('<str:username>/', GetCurrentUserAPIView.as_view(), name='user-detail'),
]
