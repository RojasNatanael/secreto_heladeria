# views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Empleado, Departamento, Afp, Salud
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def lista_empleados(request):
    search = request.GET.get("search", "")
    departamento = request.GET.get("departamento", "")
    afp = request.GET.get("afp", "")
    salud = request.GET.get("salud", "")

    empleados = Empleado.objects.all().select_related(
        'departamento', 
        'afp', 
        'salud',
        'informacion_personal',
        'informacion_personal__contacto'
    )

    # Debug print
    print(f"Total empleados: {empleados.count()}")

    # Text search
    if search:
        empleados = empleados.filter(
            Q(informacion_personal__nombre__icontains=search) |
            Q(informacion_personal__apellido__icontains=search) |
            Q(informacion_personal__segundo_nombre__icontains=search) |
            Q(informacion_personal__segundo_apellido__icontains=search) |
            Q(informacion_personal__contacto__correo__icontains=search) |
            Q(informacion_personal__run__icontains=search)
        )
        print(f"After search filter: {empleados.count()}")

    # Filters
    if departamento:
        empleados = empleados.filter(departamento_id=departamento)
        print(f"After departamento filter: {empleados.count()}")

    if afp:
        empleados = empleados.filter(afp_id=afp)
        print(f"After AFP filter: {empleados.count()}")

    if salud:
        empleados = empleados.filter(salud_id=salud)
        print(f"After salud filter: {empleados.count()}")

    # Pagination (25 per page)
    paginator = Paginator(empleados, 25)
    page = request.GET.get("page")
    empleados_page = paginator.get_page(page)

    context = {
        "empleados": empleados_page,
        "departamentos": Departamento.objects.all(),
        "afps": Afp.objects.all(),
        "saluds": Salud.objects.all(),
        "search": search,
        "selected_departamento": departamento,
        "selected_afp": afp,
        "selected_salud": salud,
    }
    return render(request, "lista_empleados.html", context)
