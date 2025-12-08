from django.shortcuts import render, redirect
from .forms.empleado import RegistroEmpleadoWrapper
from .forms.afp import AfpForm
from .forms.departamento import DepartamentoForm
from .forms.asistencia import AsistenciaForm
from .forms.remuneracion import RemuneracionForm
from .forms.salud import SaludForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

@permission_required('recursos_humanos.add_empleado', raise_exception=True)
def registrar_empleado(request):
    if request.method == "POST":
        wrapper = RegistroEmpleadoWrapper(request.POST, request.FILES)

        if wrapper.is_valid():
            wrapper.save()
            messages.success(request, "Empleado registrado correctamente.")
            return redirect("dashboard")
        
        for f in [
                wrapper.user_form,
                wrapper.contacto_form,
                wrapper.info_form,
                wrapper.empleado_form,
                ]:
            for field, errors in f.errors.items():
                for err in errors:
                    messages.error(request, f"{field}: {err}")

    else:
        wrapper = RegistroEmpleadoWrapper()

    return render(request, "registrar_empleado.html", {
        "user_form": wrapper.user_form,
        "contacto_form": wrapper.contacto_form,
        "info_form": wrapper.info_form,
        "empleado_form": wrapper.empleado_form,
    })

@permission_required('recursos_humanos.add_afp',raise_exception=True)
def registrar_afp(request):
    if request.method == "POST":
        form = AfpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "AFP registrada correctamente.")
            return redirect("registrar_afp")
    else:
        form = AfpForm()

    return render(request, "registrar_afp.html", {"afp_form": form})

@permission_required('recursos_humanos.add_departamento',raise_exception=True)
def registrar_departamento(request):
    if request.method == "POST":
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento registrado correctamente.")
            return redirect("registrar_departamento")
    else:
            form = DepartamentoForm()
        
    return render(request, "registrar_departamento.html", {"departamento_form":form})
@permission_required('recursos_humanos.add_asistencia', raise_exception=True)
def registrar_asistencia(request):
    if request.method == "POST":
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asistencia registrada correctamente.")
            return redirect("registrar_asistencia")
        else:
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, f"{field}: {err}")
    else:
        form = AsistenciaForm()
    return render(request, "registrar_asistencia.html", {"asistencia_form":form})

@permission_required('recursos_humanos.add_remuneracion',raise_exception=True)
def registrar_remuneracion(request):
    if request.method == "POST":
        form = RemuneracionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Remuneracion registrada correctamente")
            return redirect("registrar_remuneracion")
    else:
            form = RemuneracionForm()
        
    return render(request, "registrar_remuneracion.html", {"remuneracion_form":form})

@permission_required('recursos_humanos.add_salud',raise_exception=True)
def registrar_salud(request):
    if request.method == "POST":
        form = SaludForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aseguradora registrada correctamente.")
            return redirect("registrar_salud")
    else:
            form = SaludForm()
        
    return render(request, "registrar_salud.html", {"salud_form":form})

@login_required
def dashboard(request):
    return render(request, "dashboard.html")
