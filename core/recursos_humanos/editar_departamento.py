from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Departamento
from .forms.departamento import DepartamentoForm


def editar_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)

    if request.method == "POST":
        form = DepartamentoForm(request.POST, instance=departamento)

        if form.is_valid():
            form.save()
            messages.success(request, "Departamento actualizado correctamente.")
            return redirect("departamentos_listar")
        else:
            messages.error(request, "Hay errores en el formulario (눈_눈).")

    else:
        form = DepartamentoForm(instance=departamento)

    return render(request, "editar_departamento.html", {"form": form})

