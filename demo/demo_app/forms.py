from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from topnotchdev.files_widget.forms.fields import ImagesFormField

from .models import MyModel, MyModelTwoFields


class DemoImagesForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ["images"]
        labels = {'images': ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # Uncomment respectively to see result (drag and drop, sorting, input button)
        # self.fields["images"].disabled = True
        # self.fields["images"].widget.attrs['readonly'] = "readonly"

        self.helper.layout.append(Submit("Submit", "submit"))


class DemoImagesTwoImageFieldsForm(forms.ModelForm):
    class Meta:
        model = MyModelTwoFields
        fields = ["avatar", "scene", "place"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # Uncomment respectively to see result (drag and drop, sorting, input button)

        # self.fields["scene"].disabled = True
        self.fields["avatar"].widget.template = "demo_app/my_image_widget_template.html"
        # self.fields["avatar"].widget.attrs['readonly'] = "readonly"

        self.helper.layout.append(Submit("Submit", "submit"))


class Demo3NonModelForm(forms.Form):
    avatar = ImagesFormField(required=True, label=_("Avatar"))
    nickname = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(Demo3NonModelForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"

        self.helper.add_input(
                Submit("submit", _("Submit")))
