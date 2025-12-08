# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from .models import Empleado, Departamento, Afp, Salud
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404


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

@permission_required('recursos_humanos.delete_empleado', raise_exception=True)
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    empleado_nombre = f"{empleado.informacion_personal.nombre} {empleado.informacion_personal.apellido}"
    
    try:
        # Verificar manualmente si hay registros relacionados primero
        # Esto es más informativo y controlado
        registros_relacionados = []
        
        if empleado.asistencias.exists():
            registros_relacionados.append("asistencias")
        
        if empleado.remuneraciones.exists():
            registros_relacionados.append("remuneraciones")
        
        # Agrega más verificaciones según tus modelos relacionados
        # Por ejemplo, si tienes otros modelos con PROTECT
        
        if registros_relacionados:
            tipos_str = ", ".join(registros_relacionados)
            messages.error(
                request, 
                f'No es posible eliminar al empleado {empleado_nombre} porque tiene registros guardados: {tipos_str}.'
            )
        else:
            empleado.delete()
            messages.success(request, f'Empleado {empleado_nombre} eliminado correctamente.')
            
    except ProtectedError:
        # Fallback en caso de que Django detecte otras protecciones
        messages.error(
            request, 
            f'No es posible eliminar al empleado {empleado_nombre} porque tiene registros relacionados que lo protegen.'
        )
    
    except Exception as e:
        messages.error(request, f'Error al eliminar empleado: {str(e)}')
    
    return redirect('lista_empleados')
