from django.urls import path
from . import views


urlpatterns = [
    path('stat', views.market_stat_view),
    path('market_index', views.market_index_view),
]
