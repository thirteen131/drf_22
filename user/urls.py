from django.urls import path

from user import views

urlpatterns = [
    path("users/", views.UserAPIView.as_view()),
    path("users/<str:id>/", views.UserAPIView.as_view()),

    path("employee/", views.EmployeeAPIView.as_view()),
    path("employee/<str:id>/", views.EmployeeAPIView.as_view()),
]
