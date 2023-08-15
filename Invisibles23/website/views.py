from django.shortcuts import render
from django.views import View
from Invisibles23.logging_config import logger
from django.urls import reverse
from .forms import MembershipForm
from datetime import date
from .models import (
    HomeSections,
    AboutSections,
    AssoSections,
    ChronicTabSections,
    InvsibleTabSections,
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
    MiscarriageTabSections,
    YoutubeVideos,
    Event,
    ContactSection,
    AssoStatus,
)
from .filters import (
    AdminRessourcesFilter,
    TherapeuticRessourcesFilter,
    FinancialRessourcesFilter,
)
from django.http import JsonResponse
import environ
import requests
from django.middleware.csrf import get_token
from django.conf import settings
from django.shortcuts import redirect

# Initialise env vars
env = environ.Env()
env.read_env("../.env")

# == Base view classes to stay DRY == #
class BaseThematicView(View):
    """
    Base class for the thematic views
    """

    template_name = None
    # queryset = None

    def get_queryset(self):
        return {
            "sections_content": getattr(self, "model", None).objects.exclude(
                order=0
            )  # Get section from the given model
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class BaseRessourcesView(View):
    """
    Base class for the ressources views
    """

    template_name = "website/ressources.html"
    filter_class = None

    def get_queryset(self):
        queryset = getattr(
            self, "model", None
        ).objects.all()  # Get all objects from the given model
        return queryset

    def get_context_data(self):
        filter_form = self.filter_class(self.request.GET, queryset=self.get_queryset())
        ressources = filter_form.qs
        return {"ressources": ressources, "filter_form": filter_form}

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)


# == Views == #
class HomeView(View):
    template_name = "website/home.html"
    # queryset = HomeSections.objects.all()
    # contact_query = ContactSection.objects.first() # For the contact form

    def get_queryset(self):
        # return Home section and contact section queryset
        return {
            "sections_content": HomeSections.objects.all(),
            "contact_content": ContactSection.objects.first(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "website/about.html"

    def get_queryset(self):
        # return About section and all videos queryset
        return {
            "sections_content": AboutSections.objects.all(),
            "videos": YoutubeVideos.objects.all(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class ChronicTabView(BaseThematicView):
    template_name = "website/chronic.html"
    model = ChronicTabSections  # Model to query


class InvisibleTabView(BaseThematicView):
    template_name = "website/invisible.html"
    model = InvsibleTabSections  # Model to query


class MiscarriageTabView(BaseThematicView):
    template_name = "website/miscarriage.html"
    model = MiscarriageTabSections  # Model to query


class PodcastsView(View):
    template_name = "website/podcasts.html"

    def get(self, request):
        return render(request, self.template_name, {})


class AdminRessourcesView(BaseRessourcesView):
    model = AdminRessources
    filter_class = AdminRessourcesFilter


class TherapeuticRessourcesView(BaseRessourcesView):
    model = TherapeuticRessources
    filter_class = TherapeuticRessourcesFilter


class FinancialRessourcesView(BaseRessourcesView):
    model = FinancialRessources
    filter_class = FinancialRessourcesFilter


class AssociationView(View):
    template_name = "website/association.html"

    def get_queryset(self):
        return {
            "sections_content": AssoSections.objects.all(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class EventListView(View):
    template_name = "website/events-list.html"
    queryset = Event.objects.all()

    def get_queryset(self):
        # Get future events and order them by date
        return {
            "events_content": self.queryset.filter(date__gte=date.today()).order_by(
                "date"
            ),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class EventDetailView(View):
    template_name = "website/event-detail.html"

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        context = {
            "event": event,
        }
        return render(request, self.template_name, context)


class ContactView(View):
    template_name = "website/contact.html"
    
    def get_queryset(self):
        # return Home section and contact section queryset
        return {
            "contact_content": ContactSection.objects.first(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class MembershipView(View):
    template_name = "website/membership.html"
    form_class = MembershipForm()
    initial_form_state = {"subscription": "normal", "frequency": "yearly"} # Default state of radio buttons

    def get(self, request):
        form = MembershipForm(initial=self.initial_form_state)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MembershipForm(request.POST)
        domain = "http://127.0.0.1:8000" if settings.DEBUG else f"https://{settings.DOMAIN}"
        stripeProxy_url = reverse("stripe-proxy")
        logger.info(f"Will send request to {domain}{stripeProxy_url}")
        logger.debug(f"Request data: {request.POST}")

        if form.is_valid():
            logger.info("Membership form is valid")
            subscription = form.cleaned_data["subscription"]
            frequency = form.cleaned_data["frequency"]
            first_name = form.cleaned_data["fname"]
            last_name = form.cleaned_data["lname"]
            birthday = form.cleaned_data["birthday"]
            address = form.cleaned_data["address"]
            zip_code = form.cleaned_data["zip_code"]
            city = form.cleaned_data["city"]
            email = form.cleaned_data["email"]
            lookup_key = request.POST.get("lookup_key")
            csrf_token = request.COOKIES.get(settings.CSRF_COOKIE_NAME)

            # Create the request to send to the proxy server
            headers = {
                "X-CSRFToken": csrf_token,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            data = {
                "lookup_key": lookup_key,
                "subscription": subscription,
                "frequency": frequency,
                "fname": first_name,
                "lname": last_name,
                "birthday": birthday,
                "address": address,
                "zip_code": zip_code,
                "city": city,
                "email": email,
            }

            # Print headers and data for debugging
            logger.debug(f"Form submission headers: {headers}")
            logger.debug(f"Form submission data: {data}")
            logger.debug(f"Cookie: {request.COOKIES}")

            try:
                # Get the session url from the proxy server
                response = requests.post(
                    domain + "/api/proxy/stripe/",
                    headers=headers,
                    data=data,
                    cookies=request.COOKIES,
                    allow_redirects=False,
                    timeout=60,
                )
                response_json = response.json()

                logger.debug(f"Json object: {response_json}")

                if response.status_code == 200:
                    logger.info("Session created successfully ... redirecting to checkout")
                    logger.debug(f"Session url: {response_json['sessionUrl']}")
                    return redirect(response_json["sessionUrl"], code=303)
                elif response.status_code == 409:
                    logger.warning("An error 409 occured ... redirecting to membership page")
                    logger.error(response_json["error"])
                    return render(
                        request,
                        self.template_name,
                        {"form": form, "error": response_json["error-message"]},
                    )
                elif response.status_code != 200 and response.status_code != 409:
                    logger.warning(f"An error occured, received status code: {str(response.status_code)}")
                    logger.error(response_json["error"])
                    return render(
                        request,
                        self.template_name,
                        {"form": form, "error": response_json["error-message"]},
                    )
            except Exception as e:
                logger.error(f"An error occurred while sending the request: {str(e)}")
                return render(request, self.template_name, {"form": form, "error": "An error occurred during the request."})
            
        else:
            logger.error("Form is not valid")
            error_data = form.errors.as_data()

            # convert error_data to a dict and message to a string
            error_dict = {}
            for key, value in error_data.items():
                error_dict[key] = str(value[0].message)

            # Create error_ul from error_dict
            error_ul = "<ul><li>" + "</li><li>".join(error_dict.values()) + "</li></ul>"

            # pass error_ul to the template as html
            error_context = {
                "form": form,
                "error_inputs": error_dict.keys(),
                "error_messages": error_ul,
            }

            return render(request, self.template_name, error_context)


class StatusView(View):
    template_name = "website/status.html"

    def get_queryset(self):
        # return Home section and contact section queryset
        return AssoStatus.objects.first()

    def get(self, request):
        context = {
            "status_content": self.get_queryset(),
        }
        return render(request, self.template_name, context)


class SuccessView(View):
    template_name = "website/success.html"

    def get(self, request):
        logger.info("Payment successful ... redirecting to success page")
        return render(request, self.template_name, {})


def get_sensitive_info(request):
    data = {
        "ausha_api_token": env("AUSHA_API_TOKEN"),
        "mailchimp_api_key": env("MAILCHIMP_API_KEY"),
        "mailchimp_list_id": env("MAILCHIMP_LIST_ID"),
        "emailjs_service_id": env("EMAILJS_SERVICE_ID"),
        "emailjs_template_id": env("EMAILJS_TEMPLATE_ID"),
        "emailjs_user_id": env("EMAILJS_USER_ID"),
    }

    return JsonResponse(data)
