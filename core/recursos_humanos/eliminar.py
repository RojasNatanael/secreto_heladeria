from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.urls import reverse
from .models import Empleado

def eliminar_empleado(request, id):
    """Vista para mostrar información antes de eliminar"""
    empleado = get_object_or_404(Empleado, id=id)
    
    # Verificar todas las dependencias posibles
    dependencias = []
    
    # Verificar asistencias
    if empleado.asistencias.exists():
        count = empleado.asistencias.count()
        dependencias.append(f"Asistencias: {count} registro(s)")
    
    # Verificar remuneraciones
    if empleado.remuneraciones.exists():
        count = empleado.remuneraciones.count()
        dependencias.append(f"Remuneraciones: {count} registro(s)")
    
    context = {
        'empleado': empleado,
        'dependencias': dependencias,
        'tiene_dependencias': len(dependencias) > 0
    }
    
    return render(request, 'confirmar_eliminar_empleado.html', context)

def eliminar_empleado(request, id):
    """Vista para eliminar el empleado"""
    empleado = get_object_or_404(Empleado, id=id)
    
    # Verificar si hay solicitud POST
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('lista_empleados')
    
    try:
        # Verificar dependencias nuevamente por seguridad
        if empleado.asistencias.exists() or empleado.remuneraciones.exists():
            messages.error(request, 'No se puede eliminar porque tiene registros asociados.')
            return redirect('confirmar_eliminar_empleado', id=id)
        
        # Guardar información para el mensaje
        nombre = f"{empleado.informacion_personal.nombre} {empleado.informacion_personal.apellido}"
        
        # Eliminar en orden correcto
        # 1. Eliminar el usuario de Django
        if empleado.user:
            empleado.user.delete()
        
        # 2. Eliminar información personal (que elimina contacto automáticamente)
        if empleado.informacion_personal:
            empleado.informacion_personal.delete()
        
        # 3. El empleado se eliminará automáticamente por CASCADE
        
        messages.success(request, f'Empleado "{nombre}" eliminado exitosamente.')
        
    except models.ProtectedError as e:
        # Capturar el error específico de PROTECT
        protected_count = len(list(e.protected_objects))
        messages.error(request, 
            f'No se puede eliminar el empleado. '
            f'Tiene {protected_count} registro(s) asociado(s) que deben eliminarse primero.')
        
        return redirect('confirmar_eliminar_empleado', id=id)
        
    except Exception as e:
        # Capturar cualquier otro error
        messages.error(request, f'Error al eliminar: {str(e)}')
        return redirect('confirmar_eliminar_empleado', id=id)
    
    return redirect('listar_empleados')

