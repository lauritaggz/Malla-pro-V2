# Convenciones de la API

REST sobre JSON bajo `/api/v1`. Cada tarea que agrega rutas las documenta en la tabla final.

## Rutas

- Recursos en plural e inglés (`/programs/{id}/curriculum`, `/me/attempts`). Los datos del usuario autenticado cuelgan de `/me/...`; así no hay ids de usuario en la URL.
- `GET` lee, `POST` crea, `PATCH` modifica (con `version`, ADR-0009), `DELETE` borra.
- Toda ruta declara su dependencia: pública, `get_current_user` o guardia de rol.
- Respuestas con `response_model` de Pydantic. Nunca se devuelve un modelo de SQLAlchemy completo sin esquema.

## Errores

Se mantiene el formato de FastAPI, que el frontend ya interpreta:

```json
{ "detail": "Este dato cambió en otro dispositivo. Recarga para ver la versión más reciente." }
```

| HTTP | Cuándo | Nota |
|---|---|---|
| 400 / 422 | Entrada inválida | 422 lo genera Pydantic; el frontend debe mostrar un mensaje legible |
| 401 | Sin token o token inválido | El frontend refresca el token y reintenta una vez |
| 403 | Autenticado sin el rol necesario | |
| 404 | No existe **o** no es del usuario | No se revela cuál de los dos |
| 409 | `version` desactualizada o duplicado | Incluye el estado actual cuando aplica |
| 429 | Límite de frecuencia | |
| 500 | Error interno | El detalle va al log, nunca a la respuesta |

## Rutas privadas y aislamiento (T-004)

Toda ruta que depende de `get_current_user` se registra en `backend/tests/isolation/registry.py`, en el mismo PR que la crea:

- **`PRIVATE_RESOURCES`**: datos de un usuario (perfil, intentos, notas, horario…). Se declara cómo crearlo, cómo lo lee su dueño y qué intentará otro usuario: leer, modificar y borrar, con el id en la URL **y** en el cuerpo (`Op(..., json={"profile_id": "{id}"})`). `assert_isolated` exige 404 en cada intento y que el recurso del dueño quede igual.
- **`SELF_SCOPED_ROUTES`**: rutas que solo actúan sobre quien llama y no reciben ids (como `GET /me`).

`tests/isolation/test_isolation.py` falla si aparece una ruta privada sin registrar (también si la protección viene de una dependencia anidada o de las dependencias del router) o si queda registrada una ruta que ya no existe. En las pruebas, `user_a` y `user_b` son clientes autenticados con tokens falsos (`fake_firebase`), sin llamar a Google.

## Idempotencia

Los `POST` que crean recursos aceptan la cabecera `Idempotency-Key` (hay que agregarla a `allow_headers` de CORS en la tarea que la implemente).

## Rutas existentes

| Método y ruta | Acceso | Tarea |
|---|---|---|
| `GET /api/v1/health` | pública | s01 |
| `GET /api/v1/me` | usuario | s02 |
| `GET /api/v1/universities` | pública, caché 5 min | s03 |
| `GET /api/v1/universities/{slug}/programs` | pública, caché 5 min | s03 |
| `GET /api/v1/programs/{program_id}/curriculum` | pública, caché 5 min | s03; T-010 agrega `version.attrs` |

### `GET /programs/{program_id}/curriculum` · `version.attrs`

Objeto con los campos del archivo de la malla que no tienen columna, tal como vienen: `universidad`, `fuente_oficial` (UNAB: `programa`, `catalogo`, `catalogoTexto`, `lectura`; U. de Chile: `documento`, `origen` o `url`, `decreto`, `sha256`, `lectura`, `verificada`), `nota_codigos`, `equivalencias` (`{código: [[códigos antiguos], …]}`, cada grupo interno es un "y") y cualquier otra clave de primer nivel. Es `{}` si no hay nada. Es informativo: ninguna regla académica lo usa todavía.
