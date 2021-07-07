from django.urls import reverse
from django.views import generic

from .forms import DemoImagesForm, DemoImagesTwoImageFieldsForm
from .models import MyModel, MyModelTwoFields


class ImagesWidgetCreateView(generic.CreateView):
    form_class = DemoImagesForm
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Create Images (one field)"
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


class ImagesWidgetTwoFieldsCreateView(generic.CreateView):
    form_class = DemoImagesTwoImageFieldsForm
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Create Images (two image fields)"
        return context

    def get_success_url(self):
        return reverse("demo2-update", kwargs={"pk": self.object.pk})


class ImagesWidgetTwoFieldsUpdateView(generic.UpdateView):
    model = MyModelTwoFields
    form_class = DemoImagesTwoImageFieldsForm
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Update Images (two image fields)"
        return context
