from django.shortcuts import render, redirect, get_object_or_404
from .models import Asistencia
from django.db.models import Q, ProtectedError
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


@login_required
def eliminar_asistencia(request, asistencia_id):
    asistencia = get_object_or_404(Asistencia, id=asistencia_id)
    
    try:
        # Obtener información antes de eliminar
        empleado_nombre = f"{asistencia.empleado.informacion_personal.nombre} {asistencia.empleado.informacion_personal.apellido}"
        fecha = asistencia.fecha
        
        # Intentar eliminar
        asistencia.delete()
        messages.success(request, f'Asistencia del {fecha} para {empleado_nombre} eliminada correctamente.')
    
    except ProtectedError:
        # En caso de que la asistencia esté protegida por otros registros
        messages.error(
            request, 
            'No es posible eliminar la asistencia porque tiene registros relacionados.'
        )
    
    except Exception as e:
        messages.error(request, f'Error al eliminar asistencia: {str(e)}')
    
    # Redirigir manteniendo los parámetros de filtro
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return redirect(referer_url)
    return redirect('lista_asistencias')
