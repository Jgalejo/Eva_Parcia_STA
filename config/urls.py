from django.contrib import admin
from django.urls import path
from presentation.views import (
    LoteCultivoView,
    ProcesoTransformacionView,
    TransporteView,
    EntregaView,
    dashboard_view
)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    
    # API Endpoints

    path('api/lotes/', LoteCultivoView.as_view(), name='lotes-list'),
    path('api/lotes/<int:lote_id>/', LoteCultivoView.as_view(), name='lotes-detail'),
    path('api/procesos/', ProcesoTransformacionView.as_view(), name='procesos-create'),
    path('api/transportes/', TransporteView.as_view(), name='transportes-create'),
    path('api/entregas/<int:transporte_id>/', EntregaView.as_view(), name='entregas-create'),
]