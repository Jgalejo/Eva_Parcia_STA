from rest_framework import serializers
from datetime import datetime, date

class LoteCultivoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    codigo_lote = serializers.CharField(max_length=50)
    finca = serializers.CharField(max_length=200)
    variedad = serializers.CharField(max_length=100)
    hectareas = serializers.DecimalField(max_digits=5, decimal_places=2)
    fecha_siembra = serializers.DateField()
    fecha_cosecha = serializers.DateField()
    responsable = serializers.CharField(max_length=200)
    certificacion_organica = serializers.BooleanField(default=True)
    
    # SOLUCIÓN: Usar validate() en lugar de validate_fecha_cosecha
    def validate(self, data):
        """
        Validación a nivel de objeto. Aquí ambos campos ya son objetos date.
        """
        fecha_siembra = data.get('fecha_siembra')
        fecha_cosecha = data.get('fecha_cosecha')
        
        if fecha_siembra and fecha_cosecha:
            if fecha_cosecha <= fecha_siembra:
                raise serializers.ValidationError({
                    "fecha_cosecha": "La fecha de cosecha debe ser posterior a la fecha de siembra"
                })
        return data


class ProcesoTransformacionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    lote_id = serializers.IntegerField()
    fecha_lavado = serializers.DateTimeField()
    responsable_lavado = serializers.CharField(max_length=200)
    metodo_lavado = serializers.CharField(max_length=100)
    fecha_empaquetado = serializers.DateTimeField()
    tipo_empaque = serializers.CharField(max_length=100)
    cantidad_empaquetada = serializers.IntegerField(min_value=1)
    unidad_medida = serializers.CharField(max_length=50)
    
    # SOLUCIÓN: Usar validate() para comparar fechas de lavado y empaquetado
    def validate(self, data):
        fecha_lavado = data.get('fecha_lavado')
        fecha_empaquetado = data.get('fecha_empaquetado')
        
        if fecha_lavado and fecha_empaquetado:
            # Validación 1: Orden cronológico
            if fecha_empaquetado <= fecha_lavado:
                raise serializers.ValidationError({
                    "fecha_empaquetado": "El empaquetado debe realizarse después del lavado"
                })
            
            # Validación 2: Tiempo máximo (24 horas)
            diferencia = fecha_empaquetado - fecha_lavado
            if diferencia.total_seconds() > 86400:  # 24 horas en segundos
                raise serializers.ValidationError({
                    "fecha_empaquetado": "El empaquetado no debe realizarse más de 24 horas después del lavado"
                })
                
        return data


class TransporteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
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
        # Aquí 'value' es Decimal, así que la comparación numérica funciona bien
        if value < 10 or value > 15:
            raise serializers.ValidationError(
                "La temperatura promedio debe estar entre 10°C y 15°C para mangos"
            )
        return value


class EntregaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fecha_entrega = serializers.DateTimeField(default=datetime.now)
    recibido_por = serializers.CharField(max_length=200)
    estado_entrega = serializers.CharField(max_length=50, default='ENTREGADO')