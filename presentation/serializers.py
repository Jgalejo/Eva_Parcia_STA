from rest_framework import serializers
from datetime import datetime, date


class LoteCultivoSerializer(serializers.Serializer):
    codigo_lote = serializers.CharField(max_length=50)
    finca = serializers.CharField(max_length=200)
    variedad = serializers.CharField(max_length=100)
    hectareas = serializers.DecimalField(max_digits=5, decimal_places=2)
    fecha_siembra = serializers.DateField()
    fecha_cosecha = serializers.DateField()
    responsable = serializers.CharField(max_length=200)
    certificacion_organica = serializers.BooleanField(default=True)
    
    def validate_fecha_cosecha(self, value):
        fecha_siembra = self.initial_data.get('fecha_siembra')
        if fecha_siembra and value <= fecha_siembra:
            raise serializers.ValidationError(
                "La fecha de cosecha debe ser posterior a la fecha de siembra"
            )
        return value


class ProcesoTransformacionSerializer(serializers.Serializer):
    lote_id = serializers.IntegerField()
    fecha_lavado = serializers.DateTimeField()
    responsable_lavado = serializers.CharField(max_length=200)
    metodo_lavado = serializers.CharField(max_length=100)
    fecha_empaquetado = serializers.DateTimeField()
    tipo_empaque = serializers.CharField(max_length=100)
    cantidad_empaquetada = serializers.IntegerField(min_value=1)
    unidad_medida = serializers.CharField(max_length=50)
    
    def validate_fecha_empaquetado(self, value):
        fecha_lavado = self.initial_data.get('fecha_lavado')
        if fecha_lavado and value <= fecha_lavado:
            raise serializers.ValidationError(
                "El empaquetado debe realizarse después del lavado"
            )
        
        if fecha_lavado and (value - fecha_lavado).total_seconds() > 86400:  # 24 horas
            raise serializers.ValidationError(
                "El empaquetado no debe realizarse más de 24 horas después del lavado"
            )
        
        return value


class TransporteSerializer(serializers.Serializer):
    lote_id = serializers.IntegerField()
    proceso_id = serializers.IntegerField()
    fecha_salida = serializers.DateTimeField()
    vehiculo = serializers.CharField(max_length=100)
    conductor = serializers.CharField(max_length=200)
    destino = serializers.CharField(max_length=200)
    temperatura_minima = serializers.DecimalField(max_digits=4, decimal_places=1, min_value=-20)
    temperatura_maxima = serializers.DecimalField(max_digits=4, decimal_places=1, max_value=30)
    temperatura_promedio = serializers.DecimalField(max_digits=4, decimal_places=1)
    
    def validate_temperatura_promedio(self, value):
        if value < 10 or value > 15:
            raise serializers.ValidationError(
                "La temperatura promedio debe estar entre 10°C y 15°C para mangos"
            )
        return value


class EntregaSerializer(serializers.Serializer):
    fecha_entrega = serializers.DateTimeField(default=datetime.now)
    recibido_por = serializers.CharField(max_length=200)
    estado_entrega = serializers.CharField(max_length=50, default='ENTREGADO')