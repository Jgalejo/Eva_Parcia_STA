from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
import json
from business.services import (
    LoteService, 
    TransformacionService, 
    TransporteService
)
from .serializers import (
    LoteCultivoSerializer,
    ProcesoTransformacionSerializer,
    TransporteSerializer,
    EntregaSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class LoteCultivoView(View):
    """Vista para gestión de Lotes de Cultivo"""
    
    def get(self, request, lote_id=None):
        if lote_id:
            # Obtener trazabilidad específica
            trazabilidad, mensaje = LoteService.obtener_trazabilidad(lote_id)
            if trazabilidad:
                return JsonResponse({
                    'success': True,
                    'data': trazabilidad,
                    'message': mensaje
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': mensaje
                }, status=404)
        
        # Listar todos los lotes
        from core.repositories import LoteRepository
        lotes = LoteRepository.obtener_todos()
        data = [
            {
                'id': l.id,
                'codigo_lote': l.codigo_lote,
                'finca': l.finca,
                'fecha_cosecha': l.fecha_cosecha.isoformat(),
                'responsable': l.responsable
            }
            for l in lotes
        ]
        return JsonResponse({
            'success': True,
            'data': data,
            'count': len(data)
        })
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = LoteCultivoSerializer(data=data)
            
            if serializer.is_valid():
                # Usar el servicio de negocio
                resultado, mensaje = LoteService.crear_lote(serializer.validated_data)
                if resultado:
                    return JsonResponse({
                        'success': True,
                        'data': resultado,
                        'message': mensaje
                    }, status=201)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': mensaje
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Datos inválidos'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error en el formato JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error interno: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ProcesoTransformacionView(View):
    """Vista para gestión de Procesos de Transformación"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = ProcesoTransformacionSerializer(data=data)
            
            if serializer.is_valid():
                # Usar el servicio de negocio
                resultado, mensaje = TransformacionService.registrar_proceso(
                    serializer.validated_data
                )
                if resultado:
                    return JsonResponse({
                        'success': True,
                        'data': resultado,
                        'message': mensaje
                    }, status=201)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': mensaje
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Datos inválidos'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error en el formato JSON'
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TransporteView(View):
    """Vista para gestión de Transportes"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = TransporteSerializer(data=data)
            
            if serializer.is_valid():
                # Usar el servicio de negocio
                resultado, mensaje = TransporteService.registrar_transporte(
                    serializer.validated_data
                )
                if resultado:
                    return JsonResponse({
                        'success': True,
                        'data': resultado,
                        'message': mensaje
                    }, status=201)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': mensaje
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Datos inválidos'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error en el formato JSON'
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class EntregaView(View):
    """Vista para registrar entregas"""
    
    def post(self, request, transporte_id):
        try:
            data = json.loads(request.body)
            serializer = EntregaSerializer(data=data)
            
            if serializer.is_valid():
                # Usar el servicio de negocio
                resultado, mensaje = TransporteService.registrar_entrega(
                    transporte_id, serializer.validated_data
                )
                if resultado:
                    return JsonResponse({
                        'success': True,
                        'data': resultado,
                        'message': mensaje
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': mensaje
                    }, status=404)
            else:
                return JsonResponse({
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Datos inválidos'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error en el formato JSON'
            }, status=400)


def dashboard_view(request):
    """Vista HTML para dashboard de trazabilidad"""
    from core.repositories import LoteRepository
    lotes = LoteRepository.obtener_todos()[:10]  # Últimos 10 lotes
    
    context = {
        'lotes': lotes,
        'total_lotes': len(lotes),
        'titulo': 'Dashboard de Trazabilidad'
    }
    return render(request, 'presentation/index.html', context)