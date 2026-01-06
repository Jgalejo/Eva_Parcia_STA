from django.core.exceptions import ObjectDoesNotExist
from .models import LoteCultivo, ProcesoTransformacion, ControlCalidad, Transporte
from typing import List, Optional, Dict, Any


class LoteRepository:
    """Repositorio para operaciones CRUD de Lotes de Cultivo"""
    
    @staticmethod
    def obtener_por_id(lote_id: int) -> Optional[LoteCultivo]:
        try:
            return LoteCultivo.objects.get(id=lote_id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def obtener_por_codigo(codigo: str) -> Optional[LoteCultivo]:
        try:
            return LoteCultivo.objects.get(codigo_lote=codigo)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def obtener_todos() -> List[LoteCultivo]:
        return list(LoteCultivo.objects.all().order_by('-fecha_cosecha'))
    
    @staticmethod
    def crear(data: Dict[str, Any]) -> LoteCultivo:
        return LoteCultivo.objects.create(**data)
    
    @staticmethod
    def actualizar(lote_id: int, data: Dict[str, Any]) -> Optional[LoteCultivo]:
        try:
            lote = LoteCultivo.objects.get(id=lote_id)
            for key, value in data.items():
                setattr(lote, key, value)
            lote.save()
            return lote
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def eliminar(lote_id: int) -> bool:
        try:
            lote = LoteCultivo.objects.get(id=lote_id)
            lote.delete()
            return True
        except ObjectDoesNotExist:
            return False


class ProcesoRepository:
    """Repositorio para operaciones CRUD de Procesos de Transformación"""
    
    @staticmethod
    def obtener_por_lote(lote_id: int) -> List[ProcesoTransformacion]:
        return list(ProcesoTransformacion.objects.filter(lote_id=lote_id).order_by('-fecha_lavado'))
    
    @staticmethod
    def crear_proceso(data: Dict[str, Any]) -> ProcesoTransformacion:
        return ProcesoTransformacion.objects.create(**data)


class TransporteRepository:
    """Repositorio para operaciones CRUD de Transportes"""
    
    @staticmethod
    def obtener_por_lote(lote_id: int) -> List[Transporte]:
        return list(Transporte.objects.filter(lote_id=lote_id).order_by('-fecha_salida'))
    
    @staticmethod
    def registrar_temperatura(transporte_id: int, temperatura: float) -> Optional[Transporte]:
        try:
            transporte = Transporte.objects.get(id=transporte_id)
            # Actualizar temperaturas (esto podría expandirse para un registro histórico)
            if temperatura < transporte.temperatura_minima:
                transporte.temperatura_minima = temperatura
            if temperatura > transporte.temperatura_maxima:
                transporte.temperatura_maxima = temperatura
            transporte.save()
            return transporte
        except ObjectDoesNotExist:
            return None