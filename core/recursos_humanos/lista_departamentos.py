from django.shortcuts import render
from django.db.models import Q
from .models import Departamento

def lista_departamentos(request):
    search = request.GET.get("search", "").strip()

    departamentos = Departamento.objects.all()

    if search:
        departamentos = departamentos.filter(
            Q(nombre__icontains=search) |
            Q(desc__icontains=search)
        )

    context = {
        "departamentos": departamentos,
        "search": search,
    }

    return render(request, "lista_departamentos.html", context)

