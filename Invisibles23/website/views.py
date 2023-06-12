from django.shortcuts import render
from django.views import View
from .models import (
    HomePageSections, 
    AboutPageSections, 
    ChronicTabSections,
    InvsibleTabSections,
    MiscarriageTabSections,
    AssociationSections,
    YoutubeVideos
)

# Create your views here.
from django.http import HttpResponse

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

# Create base class for thematic tabs (stay DRY)
class ChronicTabView(View):
    template_name = "website/chronic.html"
    queryset = ChronicTabSections.objects.exclude(order=0)

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)

class InvisibleTabView(View):
    template_name = "website/invisible.html"
    queryset = InvsibleTabSections.objects.exclude(order=0)

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)
    
class MiscarriageTabView(View):
    template_name = "website/miscarriage.html"
    queryset = MiscarriageTabSections.objects.exclude(order=0)

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)

class PodcastsView(View):
    template_name = "website/podcasts.html"

    def get(self, request):    
        return render(request, self.template_name, {})

class AssociationView(View):
    template_name = "website/association.html"
    queryset = AssociationSections.objects.all()

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)