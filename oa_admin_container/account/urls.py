from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),

    path('authentication/g/', views.Authentication.as_view()),
    path('register/g/', views.Register.as_view()),
    path('code/g/', views.Code.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
