from django import forms
from ..models import Salud
from .bootstrap import Bootstrap

class SaludForm(Bootstrap, forms.ModelForm):

    class Meta:
        model = Salud
        fields = "__all__"


