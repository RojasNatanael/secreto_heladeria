from django.http import HttpResponse
import openpyxl
from django.contrib.auth.decorators import login_required
from .models import Remuneracion
@login_required
def exportar_remuneraciones(request):
    remuneraciones = Remuneracion.objects.select_related(
        "empleado",
        "empleado__informacion_personal",
        "empleado__informacion_personal__contacto"
    ).all()

    # Filtros del listado
    search = request.GET.get("search", "")
    empleado_id = request.GET.get("empleado", "")
    min_monto = request.GET.get("min_monto", "")
    max_monto = request.GET.get("max_monto", "")
    fecha = request.GET.get("fecha", "")

    if search:
        remuneraciones = remuneraciones.filter(
            Q(empleado__informacion_personal__nombre__icontains=search) |
            Q(empleado__informacion_personal__apellido__icontains=search) |
            Q(empleado__informacion_personal__run__icontains=search)
        )

    if empleado_id:
        remuneraciones = remuneraciones.filter(empleado_id=empleado_id)

    if min_monto:
        remuneraciones = remuneraciones.filter(monto__gte=min_monto)

    if max_monto:
        remuneraciones = remuneraciones.filter(monto__lte=max_monto)

    if fecha:
        remuneraciones = remuneraciones.filter(fecha=fecha)

    remuneraciones = remuneraciones.order_by("-fecha")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Remuneraciones"

    ws.append([
        "Fecha",
        "Empleado",
        "RUN",
        "Correo",
        "Monto",
        "Fecha Ingreso",
        "Salario Base",
        "Departamento"
    ])

    for r in remuneraciones:
        e = r.empleado
        ip = e.informacion_personal

        ws.append([
            r.fecha,
            f"{ip.nombre} {ip.apellido}",
            ip.run,
            ip.contacto.correo,
            r.monto,
            e.fecha_ingreso,
            e.salario_base,
            e.departamento.nombre
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=remuneraciones.xlsx"
    wb.save(response)
    return response

