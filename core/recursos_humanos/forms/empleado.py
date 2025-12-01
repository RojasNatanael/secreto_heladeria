from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..models import Contacto, InformacionPersonal, Empleado
from .bootstrap import Bootstrap


class UserForm(Bootstrap,UserCreationForm): 

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]



class ContactoForm(Bootstrap,forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["telefono1", "telefono2", "correo"]


class InfoPersonalForm(Bootstrap,forms.ModelForm):
    class Meta:
        model = InformacionPersonal
        fields = [
            "nombre",
            "segundo_nombre",
            "apellido",
            "segundo_apellido",
            "fecha_nacimiento",
            "run",
            "estado_civil",
            "nacionalidad",
            "genero"
        ]
        widgets = {
                "fecha_nacimiento":DateInput(attrs={
                    "type":"date",
                    "class":"form-control"
                    })
                }

class EmpleadoForm(Bootstrap,forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            "fecha_ingreso",
            "salario_base",
            "contrato",
            "tipo_contrato",
            "departamento",
            "salud",
            "afp"
        ]
        widgets = {
            "fecha_ingreso": DateInput(attrs={
                "type": "date",
                "class": "form-control"
            })
        }

class RegistroEmpleadoWrapper:
    def __init__(self, data=None, files=None):
        self.user_form = UserForm(data)
        self.contacto_form = ContactoForm(data)
        self.info_form = InfoPersonalForm(data)
        self.empleado_form = EmpleadoForm(data, files)

    def is_valid(self):
        return (
            self.user_form.is_valid() and
            self.contacto_form.is_valid() and
            self.info_form.is_valid() and
            self.empleado_form.is_valid()
        )

    def save(self):
        user = self.user_form.save()

        contacto = self.contacto_form.save()

        info = self.info_form.save(commit=False)
        info.contacto = contacto
        info.save()

        empleado = self.empleado_form.save(commit=False)
        empleado.user = user
        empleado.informacion_personal = info
        empleado.save()

        return empleado

