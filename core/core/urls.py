
from django.contrib import admin
from django.urls import path
from recursos_humanos.views import registrar_empleado, registrar_afp, registrar_departamento,registrar_asistencia,registrar_remuneracion,registrar_salud, dashboard, registrar_inzumo

from django.contrib.auth import views as auth_views

from recursos_humanos.lista_empleados import lista_empleados
from recursos_humanos.editar_empleado import editar_empleado
from recursos_humanos.exportar_empleados import exportar_empleados
from recursos_humanos.lista_remuneraciones import lista_remuneraciones
from recursos_humanos.exportar_remuneraciones import exportar_remuneraciones
from recursos_humanos.lista_asistencia import lista_asistencia
from recursos_humanos.exportar_asistencias import exportar_asistencias
from recursos_humanos.lista_departamentos import lista_departamentos
from recursos_humanos.editar_departamento import editar_departamento
urlpatterns = [
    path('admin/', admin.site.urls),

    path('empleados', lista_empleados, name='lista_empleados'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('empleados/registrar/', registrar_empleado, name='registrar_empleado'),
    path('afp/registrar/', registrar_afp, name='registrar_afp'),
    path('departamento/registrar/', registrar_departamento, name='registrar_departamento'),
    path('asistencia/registrar/', registrar_asistencia, name='registrar_asistencia'),
    path('remuneracion/registrar/', registrar_remuneracion, name='registrar_remuneracion'),
    path('salud/registrar/', registrar_salud, name='registrar_salud'),
    path('inzumo/registrar/', registrar_inzumo, name='registrar_inzumo'),


    path('empleados/editar/<int:empleado_id>/', editar_empleado, name='editar_empleado'),
    path('departamentos/editar<int:departamento_id>/', editar_departamento, name='editar_departamento'),

    path('remuneracion/', lista_remuneraciones, name='lista_remuneraciones'),
    path('asistencia/', lista_asistencia, name='lista_asistencia'),
    path('departamentos/', lista_departamentos, name='lista_departamentos'),

    path('empleados/exportar/', exportar_empleados, name='exportar_empleados'),
    path('asistencia/exportar/', exportar_asistencias, name='exportar_asistencias'),
    path('remuneracion/exportar/', exportar_remuneraciones, name='exportar_remuneraciones'),

    path('', dashboard, name='dashboard'),

]
