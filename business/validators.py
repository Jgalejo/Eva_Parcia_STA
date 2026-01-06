from datetime import datetime, date
from typing import Tuple, Optional
from decimal import Decimal


class TraceabilityValidator:
    """Validador para reglas de negocio del sistema de trazabilidad"""
    
    @staticmethod
    def validar_fechas_cosecha(fecha_siembra, fecha_cosecha) -> Tuple[bool, str]:
        """Valida que las fechas de siembra y cosecha sean coherentes"""
        # Convertir strings a objetos date si es necesario
        if isinstance(fecha_siembra, str):
            fecha_siembra = datetime.strptime(fecha_siembra, "%Y-%m-%d").date()
        if isinstance(fecha_cosecha, str):
            fecha_cosecha = datetime.strptime(fecha_cosecha, "%Y-%m-%d").date()
        
        if fecha_cosecha <= fecha_siembra:
            return False, "La fecha de cosecha debe ser posterior a la fecha de siembra"
        
        diferencia = (fecha_cosecha - fecha_siembra).days
        if diferencia < 90:  # Mínimo 3 meses para mangos
            return False, "El período entre siembra y cosecha es muy corto para mangos (mínimo 90 días)"
        if diferencia > 365:  # Máximo 1 año
            return False, "El período entre siembra y cosecha es muy largo (máximo 365 días)"
        
        return True, "Fechas válidas"
    
    @staticmethod
    def validar_temperatura_transporte(temperatura) -> Tuple[bool, str]:
        """Valida que la temperatura esté en rango seguro para mangos"""
        # Convertir a Decimal si es necesario
        if isinstance(temperatura, str):
            temperatura = Decimal(temperatura)
        elif isinstance(temperatura, (int, float)):
            temperatura = Decimal(str(temperatura))
        
        if temperatura < Decimal('10'):
            return False, "Temperatura demasiado baja para mangos (mínimo 10°C)"
        if temperatura > Decimal('15'):
            return False, "Temperatura demasiado alta para mangos (óptimo 10-15°C)"
        return True, "Temperatura adecuada"
    
    @staticmethod
    def validar_proceso_transformacion(fecha_lavado, fecha_empaquetado) -> Tuple[bool, str]:
        """Valida que el proceso de transformación sea coherente"""
        # Convertir strings a objetos datetime si es necesario
        if isinstance(fecha_lavado, str):
            fecha_lavado = datetime.fromisoformat(fecha_lavado.replace('Z', '+00:00'))
        if isinstance(fecha_empaquetado, str):
            fecha_empaquetado = datetime.fromisoformat(fecha_empaquetado.replace('Z', '+00:00'))
        
        if fecha_empaquetado <= fecha_lavado:
            return False, "El empaquetado debe realizarse después del lavado"
        
        diferencia_horas = (fecha_empaquetado - fecha_lavado).total_seconds() / 3600
        if diferencia_horas > 24:
            return False, "El empaquetado no debe realizarse más de 24 horas después del lavado"
        
        return True, "Proceso de transformación válido"
    
    @staticmethod
    def calcular_trazabilidad_completa(lote_id: int) -> Tuple[bool, str]:
        """Verifica si un lote tiene trazabilidad completa"""
        from core.repositories import LoteRepository, ProcesoRepository, TransporteRepository
        
        lote = LoteRepository.obtener_por_id(lote_id)
        if not lote:
            return False, "Lote no encontrado"
        
        procesos = ProcesoRepository.obtener_por_lote(lote_id)
        if not procesos:
            return False, "Falta proceso de transformación"
        
        transportes = TransporteRepository.obtener_por_lote(lote_id)
        if not transportes:
            return False, "Falta registro de transporte"
        
        # Verificar que haya al menos un control de calidad aprobado
        for proceso in procesos:
            if proceso.controles.filter(estado='A').exists():
                return True, "Trazabilidad completa"
        
        return False, "Falta control de calidad aprobado"