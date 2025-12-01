from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Empleado, Contacto, InformacionPersonal, Departamento, Salud, Afp
from .forms.empleado import ContactoForm, InfoPersonalForm, EmpleadoForm
from django.contrib import messages

@permission_required('recursos_humanos.add_empleado', raise_exception=True)
def editar_empleado(request, empleado_id):
    # Get the empleado object with all related data
    empleado = get_object_or_404(
        Empleado.objects.select_related(
            'informacion_personal',
            'informacion_personal__contacto',
            'departamento',
            'salud',
            'afp'
        ),
        id=empleado_id
    )
    
    # Get the related objects
    info_personal = empleado.informacion_personal
    contacto = info_personal.contacto
    
    if request.method == 'POST':
        # Initialize forms with POST data and existing instances
        contacto_form = ContactoForm(request.POST, instance=contacto)
        info_form = InfoPersonalForm(request.POST, instance=info_personal)
        empleado_form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        
        if contacto_form.is_valid() and info_form.is_valid() and empleado_form.is_valid():
            # Save all forms
            contacto_form.save()
            info_form.save()
            empleado_form.save()
            
            # Add success message
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('lista_empleados')  # Adjust redirect as needed
            
    else:
        # Initialize forms with existing data
        contacto_form = ContactoForm(instance=contacto)
        info_form = InfoPersonalForm(instance=info_personal)
        empleado_form = EmpleadoForm(instance=empleado)
    
    context = {
        'empleado': empleado,
        'contacto_form': contacto_form,
        'info_form': info_form,
        'empleado_form': empleado_form,
        'departamentos': Departamento.objects.all(),
        'afps': Afp.objects.all(),
        'saluds': Salud.objects.all(),
    }
    
    return render(request, 'editar_empleado.html', context)
