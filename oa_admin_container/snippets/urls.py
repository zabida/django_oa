from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),

    path('snippets/c/', views.SnippetList.as_view()),
    path('snippets/c/<int:pk>/', views.SnippetDetail.as_view()),

    path('snippets/m/', views.SnippetListMi.as_view()),
    path('snippets/m/<int:pk>/', views.SnippetDetailMi.as_view()),

    path('snippets/g/', views.SnippetListG.as_view()),
    path('snippets/g/<int:pk>/', views.SnippetDetailG.as_view()),

    path('snippets/v1/', views.SnippetViewSet.as_view({'get': 'list'})),

    path('user_token/g/', views.UserTokenListG.as_view()),
    path('user_token/g/<int:pk>/', views.UserTokenDetailG.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

router = routers.SimpleRouter()
router.register('snippets', views.SnippetViewSet, basename='snip')
