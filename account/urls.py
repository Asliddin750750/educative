from django.urls import path
from account.views import LoginView, RegisterView, ConfirmTeacherView

app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/teacher/<int:pk>/', ConfirmTeacherView.as_view(), name='confirm-teacher')
]
