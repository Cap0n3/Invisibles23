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
    path('ressources-therapeutiques/', views.TherapeuticRessourcesView.as_view(), name='therapeutic-ressources'),
    path('ressources-financieres/', views.FinancialRessourcesView.as_view(), name='financial-ressources'),
    path('rendez-vous/', views.EventListView.as_view(), name='events'),
    path('rendez-vous/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('membership/', views.MembershipView.as_view(), name='membership'),
    path('status/', views.StatusView.as_view(), name='status'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('get_sensitive_info/', views.get_sensitive_info, name='get_sensitive_info'),
]