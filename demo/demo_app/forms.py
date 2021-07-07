from django import forms
from .models import MyModel, MyModelTwoFields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
