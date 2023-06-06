from django.shortcuts import render
from django.views import View
from .models import HomePageSections, AboutPageSections

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

    def get(self, request):
        context = {
            'sections_content' : self.queryset,
        }    
        return render(request, self.template_name, context)

class PodcastsView(View):
    template_name = "website/podcasts.html"

    def get(self, request):    
        return render(request, self.template_name, {})
