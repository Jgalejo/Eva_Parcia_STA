# test_api.ps1

Write-Host "=== SISTEMA DE TRAZABILIDAD - API TESTS ==="
Write-Host ""

# 1. Crear un lote
Write-Host "1. Creando un lote de mango..."
$loteData = @{
    codigo_lote = "MANGO-2024-001"
    finca = "Finca Orgánica El Paraíso"
    variedad = "Tommy Atkins"
    hectareas = 2.5
    fecha_siembra = "2023-03-15"
    fecha_cosecha = "2024-06-20"
    responsable = "Carlos Rodríguez"
    certificacion_organica = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/lotes/" `
        -Method POST `
        -Body $loteData `
        -ContentType "application/json"
    
    Write-Host "✅ Lote creado exitosamente!"
    Write-Host "   ID: $($response.data.id)"
    Write-Host "   Código: $($response.data.codigo_lote)"
    $loteId = $response.data.id
}
catch {
    Write-Host "❌ Error al crear lote: $($_.Exception.Message)"
    Write-Host "   Detalles: $($_.ErrorDetails.Message)"
    exit
}

Write-Host ""
Write-Host "2. Obteniendo trazabilidad del lote..."
try {
    $trazabilidad = Invoke-RestMethod -Uri "http://localhost:8000/api/lotes/$loteId/" `
        -Method GET
    
    Write-Host "✅ Trazabilidad obtenida!"
    Write-Host "   Estado: $($trazabilidad.data.trazabilidad_completa)"
    Write-Host "   Mensaje: $($trazabilidad.data.mensaje_estado)"
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "=== PRUEBAS COMPLETADAS ==="