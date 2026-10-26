# ADR-0003 · Firebase solo identifica; los datos viven en Postgres

- Estado: aceptado (implementado en s02)
- Fecha: 2026-10-26

## Contexto
Los estudiantes tienen cuenta Google; no se quiere manejar contraseñas (CU-01, NF-02).

## Decisión
El frontend inicia sesión con Firebase (Google). Cada request envía el ID token como `Authorization: Bearer`. El backend lo verifica con firebase-admin (`get_current_user`) y crea o actualiza el usuario en `users`. Firebase no guarda datos de la aplicación.

## Consecuencias
- No hay sesiones propias ni cookies; el cierre de sesión es del lado de Firebase, y el token expira por sí solo.
- Toda ruta con datos de usuario depende de `get_current_user`.
- En pruebas, `verify_firebase_token` se reemplaza (monkeypatch); nunca se llama a Google.
- Correo y contraseña quedan fuera hasta que se decida lo contrario.
