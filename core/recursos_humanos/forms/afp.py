from django import forms
from ..models import Afp
from .bootstrap import Bootstrap

class AfpForm(Bootstrap, forms.ModelForm):

    class Meta:
        model = Afp
        fields = "__all__"


