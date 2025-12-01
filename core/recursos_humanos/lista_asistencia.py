from django.shortcuts import render
from .models import Asistencia
from .forms.asistencia import AsistenciaFilterForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_asistencia(request):
    asistencias = Asistencia.objects.select_related(
        "empleado",
        "empleado__informacion_personal",
        "empleado__departamento"
    )

    form = AsistenciaFilterForm(request.GET or None)

    if form.is_valid():
        empleado = form.cleaned_data.get("empleado")
        departamento = form.cleaned_data.get("departamento")
        fecha_desde = form.cleaned_data.get("fecha_desde")
        fecha_hasta = form.cleaned_data.get("fecha_hasta")

        if empleado:
            asistencias = asistencias.filter(empleado=empleado)

        if departamento:
            asistencias = asistencias.filter(empleado__departamento=departamento)

        if fecha_desde:
            asistencias = asistencias.filter(fecha__gte=fecha_desde)

        if fecha_hasta:
            asistencias = asistencias.filter(fecha__lte=fecha_hasta)

    return render(request, "lista_asistencia.html", {
        "form": form,
        "asistencias": asistencias.order_by("-fecha")
    })

