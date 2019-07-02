from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('reg', views.reg_view)

]
