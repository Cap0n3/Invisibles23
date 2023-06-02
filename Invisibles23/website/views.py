from django.shortcuts import render
from django.views import View
from .models import WebpageSection

# Create your views here.
from django.http import HttpResponse

class HomeView(View):
    template_name = "website/home.html"
    queryset = WebpageSection.objects.all()

    def get(self, request):
        context = { 
            'sections_content' : self.queryset,
        }
        return render(request, self.template_name, context)
    
class PodcastsView(View):
    template_name = "website/podcasts.html"

    def get(self, request):    
        return render(request, self.template_name, {})
