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
    MembershipSection,
    DonationSection,
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

import stripe

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

    @staticmethod
    def choosePricing(subscription, frequency):
        """
        Choose the pricing based on the subscription and frequency.

        It will return following values:
        - support-monthly
        - support-yearly
        - normal-monthly
        - normal-yearly
        - reduced-monthly
        - reduced-yearly
        """
        _lookup_key = ""
        if subscription == "support":
            _lookup_key = (
                "support-monthly" if frequency == "monthly" else "support-yearly"
            )
        elif subscription == "normal":
            _lookup_key = (
                "normal-monthly" if frequency == "monthly" else "normal-yearly"
            )
        elif subscription == "reduced":
            _lookup_key = (
                "reduced-monthly" if frequency == "monthly" else "reduced-yearly"
            )
        else:
            logger.error("Invalid subscription or frequency")
            raise ValueError("Invalid subscription or frequency")

        return _lookup_key

    def get_queryset(self):
        # Text for the membership adhesion
        return {
            "sections_content": MembershipSection.objects.all(),
        }    
    
    def get(self, request):
        form = MembershipForm(initial=self.initial_form_state)
        sections = self.get_queryset()
        context = {
            "form": form,
            "sections_content": sections["sections_content"],
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MembershipForm(request.POST)
        domain = "http://127.0.0.1:8000" if settings.DEBUG else f"https://{settings.DOMAIN}"
        stripe.api_key = env("STRIPE_API_TOKEN")
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

            try:
                # Check if customer already exists
                logger.info("Checking if customer already exists ...")
                customer_search = stripe.Customer.search(
                    query=f"name:'{first_name} {last_name}' AND email:'{email}'",
                )

                # If customer exists, check if they have an active subscription
                if customer_search.data:
                    logger.info(f"Customer already exists: {customer_search.data[0]}")
                    existing_customer_id = customer_search.data[0].id
                    # Search for active subscription
                    subscription_search = stripe.Subscription.search(
                        query=f"status:'active'",
                    )
                    # Loop through subscriptions and find the one with the customer ID
                    for subscription in subscription_search.data:
                        if subscription.customer == existing_customer_id:
                            logger.warning(
                                f"Customer already has an active subscription: {subscription}"
                            )
                            return JsonResponse(
                                {
                                    "error": "Customer already exists in database.",
                                    "error-message": "Vous êtes déjà membre de notre association ! Si vous souhaitez modifier votre abonnement, veuillez nous contacter à l'adresse suivante : ",
                                },
                                status=409,
                            )

                # Get the lookup key according to the subscription and frequency
                lookup_key = self.choosePricing(subscription, frequency)

                # Get prices from Stripe
                logger.info("Getting prices from Stripe ...")
                prices = stripe.Price.list(
                    lookup_keys=[lookup_key], expand=["data.product"]
                )

                # Create checkout session to redirect to Stripe
                logger.info("Creating checkout session ...")
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            "price": prices.data[0].id,
                            "quantity": 1,
                        },
                    ],
                    currency="chf",
                    customer_email=email,
                    subscription_data={
                        "metadata": {
                            "Nom": f"{first_name} {last_name}",
                            "Anniversaire": birthday,
                            "adresse": address,
                            "CP": zip_code,
                            "Ville": city,
                            "Email": email,
                        },
                    },
                    mode="subscription",
                    success_url=domain + "/success/",
                    cancel_url=domain + "/membership/",
                )
            
                logger.info("Session created successfully ... redirecting to checkout")
                logger.debug(f"Session url: {checkout_session['url']}")
                return redirect(checkout_session["url"], code=303)

            except Exception as error:
                logger.error(f"An exception occurred: {error}")
                return render(request, self.template_name, {"form": form, "error_messages": f"An error occurred during the request. Please try again later or contact us at the following address: {settings.DEV_EMAIL}"})
            
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


class DonationView(View):
    template_name = "website/donation.html"

    def get_queryset(self):
        # Text for the donation adhesion
        return {
            "sections_content": DonationSection.objects.all(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


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
