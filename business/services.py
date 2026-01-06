from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from decimal import Decimal
from core.repositories import (
    LoteRepository, 
    ProcesoRepository, 
    TransporteRepository
)
from .validators import TraceabilityValidator


class LoteService:
    """Servicio para gestión de Lotes de Cultivo"""
    
    @staticmethod
    def crear_lote(data: Dict[str, Any]) -> Tuple[Optional[Dict], str]:
        """Crea un nuevo lote con validación de negocio"""
        try:
            # Validar fechas
            fecha_siembra = data.get('fecha_siembra')
            fecha_cosecha = data.get('fecha_cosecha')
            
            if fecha_siembra and fecha_cosecha:
                valido, mensaje = TraceabilityValidator.validar_fechas_cosecha(
                    fecha_siembra, fecha_cosecha
                )
                if not valido:
                    return None, mensaje
            
            # Crear el lote
            lote = LoteRepository.crear(data)
            return {
                'id': lote.id,
                'codigo_lote': lote.codigo_lote,
                'finca': lote.finca,
                'fecha_cosecha': lote.fecha_cosecha,
                'responsable': lote.responsable
            }, "Lote creado exitosamente"
        except Exception as e:
            return None, f"Error al crear lote: {str(e)}"
    
    @staticmethod
    def obtener_trazabilidad(lote_id: int) -> Tuple[Optional[Dict], str]:
        """Obtiene la trazabilidad completa de un lote"""
        try:
            lote = LoteRepository.obtener_por_id(lote_id)
            if not lote:
                return None, "Lote no encontrado"
            
            # Verificar trazabilidad completa
            completa, mensaje = TraceabilityValidator.calcular_trazabilidad_completa(lote_id)
            
            # Obtener datos relacionados
            procesos = ProcesoRepository.obtener_por_lote(lote_id)
            transportes = TransporteRepository.obtener_por_lote(lote_id)
            
            trazabilidad = {
                'lote': {
                    'id': lote.id,
                    'codigo': lote.codigo_lote,
                    'finca': lote.finca,
                    'fecha_cosecha': lote.fecha_cosecha.isoformat() if lote.fecha_cosecha else None,
                    'responsable': lote.responsable,
                    'variedad': lote.variedad
                },
                'procesos': [
                    {
                        'id': p.id,
                        'fecha_lavado': p.fecha_lavado.isoformat() if p.fecha_lavado else None,
                        'fecha_empaquetado': p.fecha_empaquetado.isoformat() if p.fecha_empaquetado else None,
                        'tipo_empaque': p.tipo_empaque,
                        'controles_calidad': [
                            {
                                'fecha': c.fecha_control.isoformat() if c.fecha_control else None,
                                'inspector': c.inspector,
                                'estado': c.get_estado_display(),
                                'brix': str(c.brix) if c.brix else None
                            }
                            for c in p.controles.all()
                        ]
                    }
                    for p in procesos
                ],
                'transportes': [
                    {
                        'id': t.id,
                        'fecha_salida': t.fecha_salida.isoformat() if t.fecha_salida else None,
                        'fecha_entrega': t.fecha_entrega.isoformat() if t.fecha_entrega else None,
                        'destino': t.destino,
                        'temperatura_promedio': float(t.temperatura_promedio) if t.temperatura_promedio else None,
                        'estado_entrega': t.estado_entrega
                    }
                    for t in transportes
                ],
                'trazabilidad_completa': completa,
                'mensaje_estado': mensaje
            }
            
            return trazabilidad, "Trazabilidad obtenida exitosamente"
        except Exception as e:
            return None, f"Error al obtener trazabilidad: {str(e)}"


class TransformacionService:
    """Servicio para gestión de Procesos de Transformación"""
    
    @staticmethod
    def registrar_proceso(data: Dict[str, Any]) -> Tuple[Optional[Dict], str]:
        """Registra un proceso de transformación"""
        try:
            # Validar proceso
            fecha_lavado = data.get('fecha_lavado')
            fecha_empaquetado = data.get('fecha_empaquetado')
            
            if fecha_lavado and fecha_empaquetado:
                valido, mensaje = TraceabilityValidator.validar_proceso_transformacion(
                    fecha_lavado, fecha_empaquetado
                )
                if not valido:
                    return None, mensaje
            
            # Crear el proceso
            proceso = ProcesoRepository.crear_proceso(data)
            return {
                'id': proceso.id,
                'lote_id': proceso.lote_id,
                'fecha_lavado': proceso.fecha_lavado.isoformat() if proceso.fecha_lavado else None,
                'fecha_empaquetado': proceso.fecha_empaquetado.isoformat() if proceso.fecha_empaquetado else None,
                'cantidad_empaquetada': proceso.cantidad_empaquetada,
                'tipo_empaque': proceso.tipo_empaque
            }, "Proceso registrado exitosamente"
        except Exception as e:
            return None, f"Error al registrar proceso: {str(e)}"


class TransporteService:
    """Servicio para gestión de Transportes"""
    
    @staticmethod
    def registrar_transporte(data: Dict[str, Any]) -> Tuple[Optional[Dict], str]:
        """Registra un transporte con validación de temperatura"""
        try:
            temperatura_promedio = data.get('temperatura_promedio')
            
            if temperatura_promedio:
                valido, mensaje = TraceabilityValidator.validar_temperatura_transporte(
                    temperatura_promedio
                )
                if not valido:
                    return None, mensaje
            
            # Crear el transporte
            from core.models import Transporte
            transporte = Transporte.objects.create(**data)
            return {
                'id': transporte.id,
                'lote_id': transporte.lote_id,
                'destino': transporte.destino,
                'fecha_salida': transporte.fecha_salida.isoformat() if transporte.fecha_salida else None,
                'temperatura_promedio': float(transporte.temperatura_promedio) if transporte.temperatura_promedio else None
            }, "Transporte registrado exitosamente"
        except Exception as e:
            return None, f"Error al registrar transporte: {str(e)}"
    
    @staticmethod
    def registrar_entrega(transporte_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict], str]:
        """Registra la entrega final del transporte"""
        try:
            from core.models import Transporte
            transporte = Transporte.objects.get(id=transporte_id)
            
            fecha_entrega = data.get('fecha_entrega')
            if isinstance(fecha_entrega, str):
                fecha_entrega = datetime.fromisoformat(fecha_entrega.replace('Z', '+00:00'))
            
            transporte.fecha_entrega = fecha_entrega or datetime.now()
            transporte.recibido_por = data.get('recibido_por', '')
            transporte.estado_entrega = data.get('estado_entrega', 'ENTREGADO')
            transporte.save()
            
            return {
                'id': transporte.id,
                'fecha_entrega': transporte.fecha_entrega.isoformat() if transporte.fecha_entrega else None,
                'recibido_por': transporte.recibido_por,
                'estado': transporte.estado_entrega
            }, "Entrega registrada exitosamente"
        except Transporte.DoesNotExist:
            return None, "Transporte no encontrado"
        except Exception as e:
            return None, f"Error al registrar entrega: {str(e)}"