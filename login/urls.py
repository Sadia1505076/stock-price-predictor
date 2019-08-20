from django.urls import path
from . import views
from home.views import home_view

urlpatterns = [
    path('reg', views.SignUpView.as_view()),
    path('home', home_view),
]
