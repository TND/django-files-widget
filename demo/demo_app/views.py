from django.urls import reverse
from django.views import generic

from .forms import DemoImagesForm
from .models import MyModel


class ImagesWidgetCreateView(generic.CreateView):
    form_class = DemoImagesForm
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Create Images"
        return context

    def get_success_url(self):
        return reverse("demo-update", kwargs={"pk": self.object.pk})


class ImagesWidgetUpdateView(generic.UpdateView):
    model = MyModel
    form_class = DemoImagesForm
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Update Images"
        return context
