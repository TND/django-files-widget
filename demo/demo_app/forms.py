from django import forms
from .models import MyModel
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
        self.fields["images"].widget.attrs['readonly'] = "readonly"

        self.helper.layout.append(Submit("Submit", "submit"))
