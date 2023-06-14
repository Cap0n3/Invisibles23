from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('a-propos/', views.AboutView.as_view(), name='about'),
    path('maladies-chroniques/', views.ChronicTabView.as_view(), name='chronic'),
    path('maladies-invisibles/', views.InvisibleTabView.as_view(), name='invisible'),
    path('fausses-couches/', views.MiscarriageTabView.as_view(), name='miscarriage'),
    path('podcasts/', views.PodcastsView.as_view(), name='podcasts'),
    path('association/', views.AssociationView.as_view(), name='association'),
    path('ressources-administratives/', views.AdminRessourcesView.as_view(), name='admin-ressources'),
]