from django.contrib import admin
from .models import (
    HomeSections,
    AboutSections,
    YoutubeVideos,
    AssoSections,
    ChronicTabSections,
    InvsibleTabSections,
    MiscarriageTabSections,
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
    Event,
    ContactSection,
    AssoStatus,
)

# Register your models here.
admin.site.register(HomeSections)
admin.site.register(AboutSections)
admin.site.register(YoutubeVideos)
admin.site.register(AssoSections)
admin.site.register(ChronicTabSections)
admin.site.register(InvsibleTabSections)
admin.site.register(MiscarriageTabSections)
admin.site.register(AdminRessources)
admin.site.register(TherapeuticRessources)
admin.site.register(FinancialRessources)
admin.site.register(Event)
admin.site.register(ContactSection)
admin.site.register(AssoStatus)
