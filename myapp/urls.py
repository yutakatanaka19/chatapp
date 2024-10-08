from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.CustomLoginView.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:param>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('s_username_change', views.suc, name='suc'),
    path('s_email_change', views.sec, name='sec'),
    path('s_icon_change', views.sic, name='sic'),
    path('s_password_change', views.CustomPasswordChangeView.as_view(), name='spc'),
    path('logout', views.CustomLogoutView.as_view(), name='logout_view'),
    path('s_change_completed', views.scc, name='scc')
]
