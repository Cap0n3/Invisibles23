from django.contrib import admin
from .models import (
    HomePageSections, 
    AboutPageSections, 
    YoutubeVideos, 
    AssociationSections
)

# Register your models here.
admin.site.register(HomePageSections)
admin.site.register(AboutPageSections)
admin.site.register(YoutubeVideos)
admin.site.register(AssociationSections)