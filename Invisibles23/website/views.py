from django.shortcuts import render
from django.views import View
from datetime import date
from .models import (
    HomePageSections, 
    AboutPageSections, 
    ChronicTabSections,
    InvsibleTabSections,
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
    MiscarriageTabSections,
    AssociationSections,
    YoutubeVideos,
    Event,
    ContactSection
)
from .filters import (
    AdminRessourcesFilter,
    TherapeuticRessourcesFilter,
    FinancialRessourcesFilter
)

# == Base view classes to stay DRY == #
class BaseThematicView(View):
    """
    Base class for the thematic views
    """
    template_name = None
    queryset = None

    def get_context_data(self):
        return {'sections_content': self.queryset}

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class BaseRessourcesView(View):
    """
    Base class for the ressources views
    """
    template_name = "website/ressources.html"
    queryset = None
    filter_class = None

    def get_context_data(self):
        filter_form = self.filter_class(self.request.GET, queryset=self.queryset)
        ressources = filter_form.qs
        return {'ressources': ressources, 'filter_form': filter_form}

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

# == Views == #
class HomeView(View):
    template_name = "website/home.html"
    queryset = HomePageSections.objects.all()
    contact_query = ContactSection.objects.first() # For the contact form

    def get(self, request):
        context = { 
            'sections_content' : self.queryset,
            'contact_content' : self.contact_query,
        }
        return render(request, self.template_name, context)

class AboutView(View):
    template_name = "website/about.html"
    queryset = AboutPageSections.objects.all()
    allVideos = YoutubeVideos.objects.all()

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
            'videos' : self.allVideos,
        }    
        return render(request, self.template_name, context)

class ChronicTabView(BaseThematicView):
    template_name = "website/chronic.html"
    queryset = ChronicTabSections.objects.exclude(order=0)

class InvisibleTabView(BaseThematicView):
    template_name = "website/invisible.html"
    queryset = InvsibleTabSections.objects.exclude(order=0)
    
class MiscarriageTabView(BaseThematicView):
    template_name = "website/miscarriage.html"
    queryset = MiscarriageTabSections.objects.exclude(order=0)

class PodcastsView(View):
    template_name = "website/podcasts.html"

    def get(self, request):    
        return render(request, self.template_name, {})

class AdminRessourcesView(BaseRessourcesView):
    queryset =  AdminRessources.objects.all()
    filter_class = AdminRessourcesFilter

class TherapeuticRessourcesView(BaseRessourcesView):
    queryset =  TherapeuticRessources.objects.all()
    filter_class = TherapeuticRessourcesFilter

class FinancialRessourcesView(BaseRessourcesView):
    queryset =  FinancialRessources.objects.all()
    filter_class = FinancialRessourcesFilter

class AssociationView(View):
    template_name = "website/association.html"
    queryset = AssociationSections.objects.all()

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)
    
class EventListView(View):
    template_name = "website/events-list.html"
    queryset = Event.objects.all()

    def get_queryset(self):
        # Get future events and order them by date
        return self.queryset.filter(date__gte=date.today()).order_by('date')
    
    def get(self, request):
        context = {
            'events_content' : self.get_queryset(),
        }    
        return render(request, self.template_name, context)
    
class EventDetailView(View):
    template_name = "website/event-detail.html"

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        context = {
            'event' : event,
        }    
        return render(request, self.template_name, context)

class ContactView(View):
    template_name = "website/contact.html"
    queryset = ContactSection.objects.first()

    def get(self, request):
        context = {
            'contact_content' : self.queryset,
        }

        return render(request, self.template_name, context)