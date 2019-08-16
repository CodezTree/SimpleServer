from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('health/', views.check_health, name="health"),
    path('articlecomp.action.keyword/', views.articlecomp_action_keyword, name="artcomp_keyword" ),
    path('articlecomp.action.keyword', views.articlecomp_action_keyword, name="artcomp_keyword" ),
    path('articlecomp.action.now/', views.articlecomp_action_now, name="artcomp_now"),
    path('articlecomp.action.now', views.articlecomp_action_now, name="artcomp_now"),
]