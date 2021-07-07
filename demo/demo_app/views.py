from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

from .forms import DemoImagesForm, DemoImagesTwoImageFieldsForm, Demo3NonModelForm
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


class Demo3GenericView(generic.FormView):
    form_class = Demo3NonModelForm
    template_name = "form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = "Generic View (no db saving)"
        return context

    def form_valid(self, form):
        result = form.cleaned_data

        context = self.get_context_data(form=form)
        context.update({"result": result})

        return self.render_to_response(context)
