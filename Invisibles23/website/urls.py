from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('a-propos/', views.AboutView.as_view(), name='about'),
    path('podcasts/', views.PodcastsView.as_view(), name='podcasts'),
    path('association/', views.AssociationView.as_view(), name='association'),
]