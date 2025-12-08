import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Empleado

@login_required
def exportar_empleados(request):
    empleados = Empleado.objects.select_related(
        'departamento',
        'afp',
        'salud',
        'informacion_personal',
        'informacion_personal__contacto',
        'user'
    ).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Empleados"

    # Encabezados completos
    ws.append([
        "Usuario (username)",
        "Nombre",
        "Segundo Nombre",
        "Apellido",
        "Segundo Apellido",
        "RUT",
        "Fecha Nacimiento",
        "Estado Civil",
        "Nacionalidad",
        "Género",
        "Teléfono 1",
        "Teléfono 2",
        "Correo",
        "Fecha Ingreso",
        "Salario Base",
        "Tipo Contrato",
        "Departamento",
        "AFP",
        "AFP % Cotización",
        "AFP % APV",
        "AFP Observaciones",
        "Salud Tipo",
        "Nombre Isapre",
        "Plan Salud",
        "Salud % Cotización",
    ])

    for e in empleados:
        ip = e.informacion_personal
        c = ip.contacto
        afp = e.afp
        salud = e.salud

        ws.append([
            e.user.username,
            ip.nombre,
            ip.segundo_nombre or "",
            ip.apellido,
            ip.segundo_apellido,
            ip.run,
            ip.fecha_nacimiento,
            ip.estado_civil,
            ip.nacionalidad,
            ip.genero,
            c.telefono1,
            c.telefono2 or "",
            c.correo,
            e.fecha_ingreso,
            e.salario_base,
            e.tipo_contrato,
            e.departamento.nombre,
            afp.nombre,
            afp.porcentaje_cotizacion,
            afp.porcentaje_apv,
            afp.observaciones or "",
            salud.tipo,
            salud.nombre_isapre or "",
            salud.plan or "",
            salud.cotizacion_porcentaje
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=empleados.xlsx"
    wb.save(response)

    return response

