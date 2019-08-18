from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('health/', views.check_health, name="health"),
    path('articlecomp.action.keyword/', views.articlecomp_action_keyword, name="artcomp_keyword" ),
    path('articlecomp.action.keyword', views.articlecomp_action_keyword, name="artcomp_keyword" ),
    path('articlecomp.action.now/', views.articlecomp_action_now, name="artcomp_now"),
    path('articlecomp.action.now', views.articlecomp_action_now, name="artcomp_now"),
    path('articlecomp.action.keyword.confirm', views.articlecomp_action_keyword_send_app, name="artcomp_now"),
    path('articlecomp.action.keyword.confirm/', views.articlecomp_action_keyword_send_app, name="artcomp_now"),
    path('register/', views.register, name="register"),
    path('register', views.register, name="register"),
    path('register.confirm', views.register_check, name="register_check"),
    path('register.confirm/', views.register_check, name="register_check"),
    path('register_app_check', views.register_app_check, name="register_app_check"),
    path('register_app_check/', views.register_app_check, name="register_app_check"),
    path('url_share_app', views.url_share_app, name="url_share_app"),
    path('url_share_app/', views.url_share_app, name="url_share_app"),
    path('articlecomp.action.now.quit', views.url_quit, name="url_quit"),
    path('articlecomp.action.now.quit/', views.url_quit, name="url_quit"),
    path('articlecomp.action.now.done', views.url_done, name="url_done"),
    path('articlecomp.action.now.done/', views.url_done, name="url_done"),
    path('articlecomp.action.now.reject', views.url_reject, name="url_done"),
    path('articlecomp.action.now.reject/', views.url_reject, name="url_done"),
    path('articlecomp.action.now.confirm', views.url_confirm, name="url_confirm"),
    path('articlecomp.action.now.confirm/', views.url_confirm, name="url_confirm"),
    path('note', views.note, name="note")
]