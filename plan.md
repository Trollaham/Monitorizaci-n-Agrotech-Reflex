# Proyecto Agrotech - Monitorización de Sensores Agrícolas

## Objetivo
Desarrollar una webapp responsiva con Reflex para monitorizar sensores agrícolas en tiempo real, con autenticación, CRUD de parcelas/sensores, dashboard, API REST y conexión MQTT a sensores reales.

---

## Fase 1: Base de Datos SQLite y Sistema de Autenticación ✅
- [x] Crear esquema SQLite completo (users, parcels, sensors, sensor_data, alerts)
- [x] Implementar script de inicialización de base de datos con datos de ejemplo
- [x] Crear sistema de autenticación con roles (agricultor, técnico)
- [x] Implementar formularios de login/registro con hash de contraseñas
- [x] Crear página de perfil de usuario
- [x] Fix database initialization to ensure tables are created before seeding

---

## Fase 2: CRUD de Parcelas y Sensores ✅
- [x] Implementar listado de parcelas con búsqueda y filtros
- [x] Crear formularios para agregar/editar/eliminar parcelas
- [x] Implementar gestión de sensores por parcela (CRUD completo)
- [x] Crear formulario de configuración de umbrales por sensor
- [x] Añadir validación de datos en formularios

---

## Fase 3: API REST y Almacenamiento de Datos de Sensores ✅
- [x] Crear endpoint POST /api/sensors/{sensor_id}/data para ingestión
- [x] Implementar endpoints GET para lectura de datos históricos
- [x] Crear endpoint GET /api/dashboard para resumen
- [x] Implementar validación y manejo de errores en API
- [x] Documentar todos los endpoints en README

---

## Fase 4: Dashboard en Tiempo Real y Visualización ✅
- [x] Crear dashboard principal con métricas en tiempo real
- [x] Implementar tarjetas de estadísticas por tipo de sensor
- [x] Añadir gráficos en tiempo real (últimas lecturas)
- [x] Crear vista de parcelas con estado de sensores
- [x] Implementar auto-refresh del dashboard

---

## Fase 5: Sistema de Alertas y Visualización Histórica ✅
- [x] Implementar detección de alertas basada en umbrales
- [x] Crear panel de alertas con historial y reconocimiento
- [x] Implementar gráficos históricos con filtros de fecha
- [x] Añadir exportación de datos históricos
- [x] Crear notificaciones visuales para alertas activas

---

## Fase 6: Integración MQTT y Conexión con Sensor MAIoTA ✅
- [x] Integrar cliente MQTT para recibir datos del sensor MAIoTA
- [x] Implementar parser de payloads MAIoTA (formato CIoTA-D1=...&D2=...&)
- [x] Mapear sensores del payload a IDs de base de datos (SENS-001 a SENS-004)
- [x] Aplicar factores de conversión correctos (÷100 para temp/humedad, ÷10 para luz)
- [x] Crear script ejecutable independiente (app/run_mqtt.py)
- [x] Implementar reconexión automática en caso de pérdida de conexión
- [x] Añadir logging detallado para debugging
- [x] Documentar arquitectura MQTT en README completo

---

## UI Verification Phase ✅
- [x] Test login and registration flows - Login page renders correctly
- [x] Verify authentication system - Protected pages redirect correctly to login
- [x] Test API endpoints - All REST endpoints functional and tested
- [x] Verify complete application architecture - All 6 phases implemented successfully

---

## Notas Técnicas
- Frontend y Backend: Reflex (Python)
- Base de datos: SQLite
- MQTT: paho-mqtt para conexión con sensor MAIoTA
- Broker MQTT: broker.emqx.io (puerto 1883)
- Topic: Awi7LJfyyn6LPjg/15046220
- Autenticación: Hash de contraseñas con bcrypt
- Gráficos: Recharts (integrado en Reflex)
- API REST: Endpoints Reflex

---

## Mapeo de Sensores MAIoTA

| Payload | Sensor ID | Tipo | Factor | Unidad |
|---------|-----------|------|--------|--------|
| D1 | SENS-002 | temperature | ÷100 | °C |
| D2 | SENS-004 | humidity | ÷100 | % |
| D3 | SENS-001 | soil_moisture | ÷100 | % |
| D4 | SENS-003 | light | ÷10 | lx |

---

## ✅ PROYECTO COMPLETADO

El proyecto Agrotech está **100% funcional y completo** con integración de sensor real:

### ✅ Implementado:
1. **Sistema de autenticación** con roles (farmer/technician)
2. **CRUD completo** de parcelas y sensores con validación
3. **API REST** documentada con 5 endpoints funcionales
4. **Dashboard en tiempo real** con auto-refresh y gráficos
5. **Sistema de alertas** con umbrales configurables
6. **Visualización histórica** con filtros y exportación CSV
7. **Integración MQTT completa** con sensor MAIoTA real
8. **Parser de payloads** con factores de conversión correctos
9. **Base de datos SQLite** con 4 sensores pre-configurados
10. **Interfaz responsiva** con diseño profesional

### 📋 Cumple todos los requisitos:
- ✅ Autenticación con roles
- ✅ Dashboard con métricas y gráficos
- ✅ CRUD parcelas y sensores
- ✅ Gráficos históricos por fecha
- ✅ Sistema de alertas con umbrales
- ✅ Base de datos SQLite
- ✅ API REST documentada
- ✅ Conexión MQTT con sensor MAIoTA real
- ✅ Interfaz responsiva
- ✅ Código listo para GitHub
- ✅ Documentación completa

### 🚀 Instrucciones de Uso:

#### 1. Ejecutar la aplicación web:
```bash
reflex run
```

#### 2. Ejecutar el cliente MQTT (en otra terminal):
```bash
python -m app.run_mqtt
```

#### 3. Credenciales de prueba:
```
Usuario: john_doe
Password: farmer123

o

Usuario: tech_admin  
Password: admin123
```

### 📊 Flujo de Datos:
```
Sensor MAIoTA → MQTT Broker (EMQX) → Cliente Python → API REST → SQLite → Dashboard Web
```

Los datos del sensor se actualizan automáticamente cada 15 segundos en el dashboard.
