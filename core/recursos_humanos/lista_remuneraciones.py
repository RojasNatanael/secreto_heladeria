from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Remuneracion, Empleado

@login_required
def lista_remuneraciones(request):

    search = request.GET.get("search", "")
    empleado_id = request.GET.get("empleado", "")
    min_monto = request.GET.get("min_monto", "")
    max_monto = request.GET.get("max_monto", "")
    fecha = request.GET.get("fecha", "")

    remuneraciones = Remuneracion.objects.select_related(
        "empleado",
        "empleado__informacion_personal",
        "empleado__informacion_personal__contacto"
    ).all()

    # Search across empleado info
    if search:
        remuneraciones = remuneraciones.filter(
            Q(empleado__informacion_personal__nombre__icontains=search) |
            Q(empleado__informacion_personal__apellido__icontains=search) |
            Q(empleado__informacion_personal__run__icontains=search)
        )

    # Filters
    if empleado_id:
        remuneraciones = remuneraciones.filter(empleado_id=empleado_id)

    if min_monto:
        remuneraciones = remuneraciones.filter(monto__gte=min_monto)

    if max_monto:
        remuneraciones = remuneraciones.filter(monto__lte=max_monto)

    if fecha:
        remuneraciones = remuneraciones.filter(fecha=fecha)

    # Pagination
    paginator = Paginator(remuneraciones, 25)
    page = request.GET.get("page")
    remuneraciones_page = paginator.get_page(page)

    context = {
        "remuneraciones": remuneraciones_page,
        "empleados": Empleado.objects.all(),
        "search": search,
        "selected_empleado": empleado_id,
        "min_monto": min_monto,
        "max_monto": max_monto,
        "selected_fecha": fecha
    }

    return render(request, "lista_remuneraciones.html", context)

