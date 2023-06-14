from django.shortcuts import render
from django.views import View
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
    YoutubeVideos
)
from .filters import (
    AdminRessourcesFilter,
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
    template_name = None
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

    def get(self, request):
        context = { 
            'sections_content' : self.queryset,
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
    template_name = "website/admin-ressources.html"
    queryset =  AdminRessources.objects.all()
    filter_class = AdminRessourcesFilter

class TherapeuticRessourcesView(BaseRessourcesView):
    #template_name = "website/therapeutic-ressources.html"
    #queryset =  TherapeuticRessources.objects.all()
    pass

class FinancialRessourcesView(BaseRessourcesView):
    #template_name = "website/financial-ressources.html"
    #queryset =  FinancialRessources.objects.all()
    pass

class AssociationView(View):
    template_name = "website/association.html"
    queryset = AssociationSections.objects.all()

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)