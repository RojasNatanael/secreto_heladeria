from django import forms
from ..models import Departamento
from .bootstrap import Bootstrap

class DepartamentoForm(Bootstrap, forms.ModelForm):

    class Meta:
        model = Departamento
        fields = "__all__"


