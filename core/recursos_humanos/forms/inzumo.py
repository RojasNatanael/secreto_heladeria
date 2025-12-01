from django import forms
from ..models import Marca, Inzumo
from .bootstrap import Bootstrap

class MarcaForm(Bootstrap, forms.ModelForm):

    class Meta:
        model = Marca
        fields = "__all__"


class InzumoForm(Bootstrap, forms.ModelForm):

    class Meta:
        model = Inzumo
        fields = "__all__"
