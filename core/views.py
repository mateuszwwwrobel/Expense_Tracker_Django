from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class BeginView(TemplateView):
    template_name = 'begin.html'


class LearnMoreView(TemplateView):
    template_name = 'learnmore.html'
