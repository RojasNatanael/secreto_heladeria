import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Asistencia
@login_required
def exportar_asistencias(request):
    asistencias = Asistencia.objects.select_related(
        "empleado",
        "empleado__informacion_personal",
        "empleado__departamento"
    )

    # Aplicar los mismos filtros del listado
    empleado = request.GET.get("empleado")
    departamento = request.GET.get("departamento")
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")

    if empleado:
        asistencias = asistencias.filter(empleado_id=empleado)

    if departamento:
        asistencias = asistencias.filter(empleado__departamento_id=departamento)

    if fecha_desde:
        asistencias = asistencias.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        asistencias = asistencias.filter(fecha__lte=fecha_hasta)

    asistencias = asistencias.order_by("-fecha")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Asistencias"

    ws.append([
        "Fecha",
        "Empleado",
        "Departamento",
        "Horas Trabajadas",
        "Horas Extra",
        "Horas Ausencia",
        "Hora Llegada",
        "Observaciones"
    ])

    for a in asistencias:
        ws.append([
            a.fecha,
            f"{a.empleado.informacion_personal.nombre} {a.empleado.informacion_personal.apellido}",
            a.empleado.departamento.nombre,
            a.horas_trabajadas,
            a.horas_extra,
            a.horas_ausencia,
            a.hora_llegada,
            a.observaciones,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=asistencias.xlsx"
    wb.save(response)
    return response

