from django.shortcuts import render
from django.views import View
from .models import WebpageSection

# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, "website/home.html")

class HomeView(View):
    template_name = "website/home.html"
    queryset = WebpageSection.objects.all()

    def get(self, request):
        context = { 'object_list' : self.queryset }
        return render(request, self.template_name, context)