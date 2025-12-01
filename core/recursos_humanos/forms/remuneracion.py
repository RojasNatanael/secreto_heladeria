from django import forms
from ..models import Remuneracion
from .bootstrap import Bootstrap
class RemuneracionForm(Bootstrap, forms.ModelForm):
    class Meta:
        model = Remuneracion
        fields = '__all__'
        help_texts = {
            'monto': 'Si no se ingresa monto, la remuneración será calculada automáticamente.'
        }
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'monto': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
            'empleado': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
