# Diagrama Relacional Actual

Este archivo documenta el diagrama relacional actual del proyecto eSports.

Archivo de imagen esperado en esta misma carpeta:

- `diagrama_relacional_actual.png`

Archivos relacionados:

- `diagrama_clases_centro_entrenamiento_v4_final.html`
- `schema_proyecto_sena.sql`

Descripcion:

El diagrama muestra la estructura actual de tablas generadas para la app `api`, incluyendo:

- `api_usuario` como tabla base
- especializaciones como `api_atleta`, `api_arbitro`, `api_administrativo`, `api_proveedor`
- relaciones de `api_sesionentrenamiento` con atleta, equipo y juego
- tablas auxiliares como `api_telefono`, `api_redsocial` y `api_acudienteatleta`
- relaciones many-to-many intermedias como `api_equipo_usuarios`, `api_equipo_trofeos` y `api_trofeo_usuarios`

Nota:

La imagen fue solicitada desde el chat, pero este entorno no me entrega el archivo binario original para guardarlo automaticamente. Si colocas la imagen con el nombre `diagrama_relacional_actual.png` dentro de `docs`, este archivo ya queda como referencia separada para esa documentacion.
