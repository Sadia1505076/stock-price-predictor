"""StockPricePredictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/', include(('home.urls', 'home'), namespace='home')),
    # url('home/', include('home.urls', namespace='home')),
    path('login/', include('login.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('search_company/', views.company_details_view),
    url(r'^home/dropdown/', include('dropdown.urls')),
]
