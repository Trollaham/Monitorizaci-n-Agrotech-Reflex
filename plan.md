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
- [x] Mapear sensores del payload a IDs de base de datos (SENS-001 a SENS-007)
- [x] Aplicar factores de conversión correctos (÷100 para temp/humedad, ÷10 para luz)
- [x] Crear script ejecutable independiente (app/run_mqtt.py)
- [x] Implementar reconexión automática en caso de pérdida de conexión
- [x] Añadir logging detallado para debugging
- [x] Documentar arquitectura MQTT en README completo
- [x] Añadir sensores de calidad de aire (CO2, VOC, NOx)
- [x] Corregir seed_database para crear todos los 7 sensores correctamente

---

## Backend Error Fixes ✅
- [x] Fix database initialization order - ensure tables created before seeding
- [x] Improve error handling in seed_database event
- [x] Add proper transaction management for database operations
- [x] Ensure all 7 sensors are properly seeded with correct data

---

## UI Verification Phase ✅
- [x] Test login and registration flows - Login page renders correctly
- [x] Verify authentication system - Protected pages redirect correctly to login
- [x] Test API endpoints - All REST endpoints functional and tested
- [x] Verify complete application architecture - All 6 phases implemented successfully
- [x] Verify all 7 sensors display correctly in dashboard with proper data

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

## Mapeo de Sensores MAIoTA (Actualizado)

| Payload | Sensor ID | Tipo | Factor | Unidad |
|---------|-----------|------|--------|--------|
| D1 | SENS-002 | temperature | ÷100 | °C |
| D2 | SENS-004 | humidity | ÷100 | % |
| D3 | SENS-001 | soil_moisture | ÷100 | % |
| D4 | SENS-003 | light | ÷10 | lx |
| D5 | SENS-005 | co2 | ÷10 | ppm |
| D6 | SENS-006 | voc | ÷10 | ppb |
| D7 | SENS-007 | nox | ÷10 | ppb |

---

## ✅ PROYECTO COMPLETADO Y BACKEND CORREGIDO

El proyecto Agrotech está **100% funcional** con el backend completamente corregido:

### ✅ Correcciones de Backend Aplicadas:
1. **Inicialización de base de datos mejorada**: Las tablas ahora se crean correctamente antes de insertar datos
2. **Manejo de errores robusto**: Transacciones con rollback automático en caso de error
3. **Validación de datos**: Se verifica la existencia de datos antes de insertarlos para evitar duplicados
4. **7 sensores configurados correctamente**: Todos los sensores (temperature, humidity, light, soil_moisture, co2, voc, nox) funcionan correctamente

### ✅ Implementado:
1. **Sistema de autenticación** con roles (farmer/technician)
2. **CRUD completo** de parcelas y sensores con validación
3. **API REST** documentada con 5 endpoints funcionales
4. **Dashboard en tiempo real** con auto-refresh cada 15 segundos
5. **Sistema de alertas** con umbrales configurables
6. **Visualización histórica** con filtros y exportación CSV
7. **Integración MQTT completa** con sensor MAIoTA real (7 sensores)
8. **Parser de payloads** con factores de conversión correctos
9. **Base de datos SQLite** con inicialización robusta y manejo de errores
10. **Interfaz responsiva** con diseño profesional

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

El backend ahora inicializa correctamente la base de datos, crea todas las tablas necesarias, y siembra los datos de ejemplo de manera robusta con manejo de errores apropiado.