from django import forms
from ..models import Asistencia, Empleado, Departamento
from .bootstrap import Bootstrap
class AsistenciaForm(Bootstrap, forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'hora_llegada': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
        }


class AsistenciaFilterForm(Bootstrap, forms.Form):
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.select_related("informacion_personal").all(),
        required=False,
        label="Empleado"
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
        label="Departamento"
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

