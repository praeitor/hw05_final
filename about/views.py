from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "../templates/about/author.html"


class AboutTechView(TemplateView):
    template_name = "../templates/about/tech.html"
