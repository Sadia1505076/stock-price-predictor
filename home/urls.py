from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('profile', views.profile_view),
    path('profile/edit/', views.update_profile),
    path('profile/changePassword/', views.change_password),

]
