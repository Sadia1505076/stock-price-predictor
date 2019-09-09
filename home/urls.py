from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name="home"),
    path('profile', views.profile_view),
    path('company_details/<trade_code>/$', views.company_details_view, name="company_detail"),
    path('profile/edit/', views.update_profile),
    path('profile/changePassword/', views.change_password),
    # path('search_company', views.company_details_view),
    path('404_not_found', views.not_found),


]
