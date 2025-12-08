from django.db import models
from django.db.models import SET_NULL, FloatField, IntegerField
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.fields import validators
from rut_chile import rut_chile


#======TEXT CHOICES======#
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

#======VALIDADORES======#
def validar_rut(rut):
    rut_limpio = rut.replace(".", "").replace("-", "").upper()

    if not rut_chile.is_valid_rut(rut_limpio):
        raise ValidationError("El RUT ingresado no es válido.")


#======MODELOS======#

class Departamento(models.Model):
    nombre = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 400)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        db_table = 'cpt_departamento'


class Contacto(models.Model):
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True,blank=True)
    correo = models.EmailField(max_length=255)
    

    def __str__(self):
        return f"Contacto {self.correo}"

    class Meta:
        db_table = 'cpt_contacto'


class InformacionPersonal(models.Model):
    nombre = models.CharField(max_length=90)
    segundo_nombre = models.CharField(max_length=90,null=True, blank=True)
    apellido = models.CharField(max_length=90)
    segundo_apellido = models.CharField(max_length=90)
    fecha_nacimiento = models.DateField()
    run = models.CharField(max_length=12, unique=True, validators = [validar_rut])
    estado_civil = models.CharField(max_length=50, choices=EstadoCivil.choices, default=EstadoCivil.SOLTERO)
    nacionalidad = models.CharField(max_length = 100)
    genero = models.CharField(max_length = 50, choices=Genero.choices, default=Genero.OTRO)
    contacto = models.OneToOneField("Contacto", on_delete=models.PROTECT, related_name='info')

    def __str__(self):
        return f"Informacion Personal {self.nombre} {self.apellido}"


#======PARA LA VALIDACION DE RUT SE ESTA USANDO UNA LIBRERIA EXTERNA======#
    def clean(self):
        if self.run:
            rut = self.run.replace(".", "").replace("-", "").upper()
            self.run = rut_chile.format_capitalized_rut_without_dots(rut)

    class Meta:
        db_table = 'cpt_informacion_personal'


class Asistencia(models.Model):
    fecha = models.DateField()
    horas_trabajadas = models.FloatField()
    horas_extra = models.FloatField()
    horas_ausencia = models.FloatField()
    hora_llegada = models.TimeField()
    observaciones = models.TextField(max_length=200)
    empleado = models.ForeignKey("Empleado", on_delete=models.PROTECT, related_name='asistencias')


    def __str__(self):
        return f"Asistencia {self.fecha} {self.empleado.informacion_personal.nombre}"

    class Meta:
        db_table = 'cpt_asistencia'
        constraints = [
                models.UniqueConstraint(
                    fields=['empleado', 'fecha'],
                    name='fecha_asistencia_unica'
                    )
                ]


class Remuneracion(models.Model):
    monto = models.IntegerField(null=True, blank=True)
    fecha = models.DateField()
    observaciones = models.TextField(max_length=500)
    empleado = models.ForeignKey("Empleado", on_delete=models.PROTECT, related_name='remuneraciones')

    def calcular_monto(self):
        empleado = self.empleado
        base = empleado.salario_base

        afp_pct = empleado.afp.porcentaje_cotizacion / 100
        afp_desc = base * afp_pct

        salud_pct = empleado.salud.cotizacion_porcentaje / 100
        salud_desc = base * salud_pct

        total = base - afp_desc - salud_desc
        return int(total)

    def save(self, *args, **kwargs):
#======SOLO CALCULA MONTO SI CAMPO SE DEJA VACIO=======#
        if not self.monto or self.monto <= 0:
            self.monto = self.calcular_monto()

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'cpt_remuneracion'




class Salud(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoSalud.choices, default=TipoSalud.FONASA)
    nombre_isapre = models.CharField(max_length=90, null=True,blank=True)
    plan = models.CharField(max_length=90, null=True,blank=True)
    cotizacion_porcentaje = models.FloatField(default=7.0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.tipo} {self.cotizacion_porcentaje}%"

    class Meta:
        db_table = 'cpt_salud'



class Afp(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    porcentaje_cotizacion = models.FloatField(validators=[MinValueValidator(0)])
    porcentaje_apv = models.FloatField(default=0, validators=[MinValueValidator(0)])
    observaciones = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        db_table = 'cpt_afp'




class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    salario_base = models.IntegerField(validators=[MinValueValidator(1, message='Salario no puede ser menor a 0')])
    contrato = models.FileField(upload_to='contratos/')
    tipo_contrato = models.CharField(max_length=50,choices=TiposContrato.choices, default=TiposContrato.INDEFINIDO,)
    departamento = models.ForeignKey("Departamento", on_delete=models.PROTECT,related_name='empleados') 
    informacion_personal = models.OneToOneField("InformacionPersonal", on_delete=models.PROTECT, related_name='empleado') 
    salud = models.ForeignKey("Salud", on_delete=models.PROTECT, related_name='empleados')
    afp = models.ForeignKey("Afp", on_delete=models.PROTECT, related_name='empleados')

    def __str__(self):
        return f"{self.informacion_personal.nombre} {self.informacion_personal.apellido}"

    class Meta:
        db_table = 'cpt_empleado'

class Marca(models.Model):
    nombre = models.CharField(max_length=90)

    def __str__(self):
        return f"{self.nombre}"
    

