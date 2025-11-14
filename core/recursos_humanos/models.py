from django.db import models
from django.db.models import SET_NULL, FloatField, IntegerField
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator
# Create your models here.

class TiposContrato(models.TextChoices):
    INDEFINIDO = "indefinido", "Contrato indefinido"
    PLAZO_FIJO = "plazo_fijo", "Contrato a plazo fijo"


class EstadoCivil(models.TextChoices):
    SOLTERO = "soltero", "Soltero(a)"
    CASADO = "casado", "Casado(a)"
    CONVIVIENTE_CIVIL = "conviviente_civil", "Conviviente civil"
    SEPARADO_JUDICIALMENTE = "separado_judicialmente", "Separado(a) judicialmente"
    DIVORCIADO = "divorciado", "Divorciado(a)"
    VIUDO = "viudo", "Viudo(a)"

class Genero(models.TextChoices):
    MASCULINO = "masculino", "masculino"
    FEMENINO = "femenino", "femenino"
    OTRO = "otro", "otro"

class TipoSalud(models.TextChoices):
    FONASA = "fonasa", "Fonasa"
    ISAPRE = "isapre", "Isapre"




class Departamento(models.Model):
    nombre = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 400)
    class Meta:
        db_table = 'cpt_departamento'


class Contacto(models.Model):
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True,blank=True)
    correo = models.EmailField(max_length=255)
    class Meta:
        db_table = 'cpt_contacto'


class InformacionPersonal(models.Model):
    nombre = models.CharField(max_length=90)
    segundo_nombre = models.CharField(max_length=90,null=True, blank=True)
    apellido = models.CharField(max_length=90)
    segundo_apellido = models.CharField(max_length=90,null=True,blank=True)
    fecha_nacimiento = models.DateField()
    run = models.CharField(max_length=10, unique=True)
    estado_civil = models.CharField(max_length=50, choices=EstadoCivil.choices, default=EstadoCivil.SOLTERO)
    nacionalidad = models.CharField(max_length = 100)
    genero = models.CharField(max_length = 50, choices=Genero.choices, default=Genero.OTRO)
    contacto = models.ForeignKey(Contacto, on_delete=SET_NULL,null=True, blank=True, related_name='info')
    class Meta:
        db_table = 'cpt_informacion_personal'


class Asistencia(models.Model):
    fecha = models.DateField()
    horas_trabajadas = models.FloatField()
    horas_extra = models.FloatField()
    horas_ausencia = models.FloatField()
    hora_llegada = models.DateTimeField()
    observaciones = models.TextField(max_length=200)
    class Meta:
        db_table = 'cpt_asistencia'


class Remuneracion(models.Model):
    monto = IntegerField()
    fecha = DateField()
    observaciones = TextField(max_length=500)

    class Meta:
        db_table = 'cpt_remuneracion'

class Salud(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoSalud.choices, default=TipoSalud.FONASA)
    nombre_isapre = models.CharField(max_length=90, null=True,blank=True)
    plan = models.CharField(max_length=90, null=True,blank=True)
    cotizacion_porcentaje = models.FloatField(default=7.0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'cpt_salud'



class Afp(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    porcentaje_cotizacion = models.FloatField(validators=[MinValueValidator(0)])
    porcentaje_apv = models.FloatField(default=0, validators=[MinValueValidator(0)])
    observaciones = models.TextField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'cpt_afp'




class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(null = True, blank = True)
    salario_base = models.IntegerField(validators=[MinValueValidator(1, message='Salario no puede ser menor a 0')])
    contrato = models.FileField(upload_to='contratos/')
    tipo_contrato = models.CharField(max_length=50,choices=TiposContrato.choices, default=TiposContrato.INDEFINIDO,)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL,null=True,blank=True,related_name='empleados') 
    informacion_personal = models.ForeignKey(InformacionPersonal, on_delete=models.SET_NULL,null=True,blank=True, related_name='empleados') 
    asistencia = models.ForeignKey(Asistencia, on_delete=SET_NULL,null=True, blank=True, related_name='empleados')
    salud = models.ForeignKey(Salud, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados')
    afp = models.ForeignKey(Afp, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados')

    class Meta:
        db_table = 'cpt_empleado'
