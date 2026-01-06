from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class LoteCultivo(models.Model):
    """Modelo para representar el origen: lote de cultivo"""
    codigo_lote = models.CharField(max_length=50, unique=True)
    finca = models.CharField(max_length=200)
    variedad = models.CharField(max_length=100)
    hectareas = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_siembra = models.DateField()
    fecha_cosecha = models.DateField()
    responsable = models.CharField(max_length=200)
    certificacion_organica = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Lote de Cultivo"
        verbose_name_plural = "Lotes de Cultivo"
    
    def __str__(self):
        return f"Lote {self.codigo_lote} - {self.finca}"


class ProcesoTransformacion(models.Model):
    """Modelo para representar la transformación: lavado, empaquetado"""
    lote = models.ForeignKey(LoteCultivo, on_delete=models.CASCADE, related_name='procesos')
    fecha_lavado = models.DateTimeField()
    responsable_lavado = models.CharField(max_length=200)
    metodo_lavado = models.CharField(max_length=100)
    fecha_empaquetado = models.DateTimeField()
    tipo_empaque = models.CharField(max_length=100)
    cantidad_empaquetada = models.IntegerField(validators=[MinValueValidator(1)])
    unidad_medida = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Proceso de Transformación"
        verbose_name_plural = "Procesos de Transformación"
    
    def __str__(self):
        return f"Transformación Lote {self.lote.codigo_lote}"


class ControlCalidad(models.Model):
    """Modelo para controles de calidad"""
    proceso = models.ForeignKey(ProcesoTransformacion, on_delete=models.CASCADE, related_name='controles')
    fecha_control = models.DateTimeField(auto_now_add=True)
    inspector = models.CharField(max_length=200)
    
    APROBADO = 'A'
    RECHAZADO = 'R'
    PENDIENTE = 'P'
    ESTADO_CHOICES = [
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (PENDIENTE, 'Pendiente'),
    ]
    
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=PENDIENTE)
    ph = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    brix = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    defectos = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Control de Calidad"
        verbose_name_plural = "Controles de Calidad"
    
    def __str__(self):
        return f"Control {self.id} - {self.get_estado_display()}"


class Transporte(models.Model):
    """Modelo para representar la logística: transporte y entrega"""
    lote = models.ForeignKey(LoteCultivo, on_delete=models.CASCADE, related_name='transportes')
    proceso = models.ForeignKey(ProcesoTransformacion, on_delete=models.CASCADE, related_name='transportes')
    fecha_salida = models.DateTimeField()
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    vehiculo = models.CharField(max_length=100)
    conductor = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    temperatura_minima = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(-20)])
    temperatura_maxima = models.DecimalField(max_digits=4, decimal_places=1, validators=[MaxValueValidator(30)])
    temperatura_promedio = models.DecimalField(max_digits=4, decimal_places=1)
    recibido_por = models.CharField(max_length=200, blank=True)
    estado_entrega = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Transporte"
        verbose_name_plural = "Transportes"
    
    def __str__(self):
        return f"Transporte Lote {self.lote.codigo_lote} a {self.destino}"