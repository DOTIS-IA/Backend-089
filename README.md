# Backend-089

Backend de sincronización para el sistema 089 (denuncias anónimas). Este repositorio contiene un job/ETL en Python que:

- Consulta conversaciones y agentes desde ElevenLabs (Conversational AI / ConvAI).
- Normaliza transcripción + metadatos + resultados de “data collection”.
- Persiste la información en PostgreSQL (tablas de `conversaciones`, `agentes` y `reportes`).

## Estructura del proyecto

- `db.py`: conexión a PostgreSQL (context manager con commit/rollback).
- `elevenlabs_client.py`: cliente HTTP para ElevenLabs + parseo de conversación.
- `sync_conversations.py`: sincronización completa (recorre conversaciones y guarda en DB).
- `.env.example`: plantilla de variables de entorno.

## Requisitos

- Python 3.10+ (recomendado)
- PostgreSQL 13+ (recomendado)
- Credenciales/API Key de ElevenLabs

Paquetes de Python usados por el proyecto:

- `requests`
- `python-dotenv`
- `psycopg2` (o `psycopg2-binary` en desarrollo)

## Configuración

### 1) Crear y activar entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Instalar dependencias

Si todavía no existe un archivo de dependencias en el repo, puedes instalar manualmente:

```bash
pip install requests python-dotenv psycopg2-binary
```

> Nota: en producción es preferible usar `psycopg2` (no *binary*) y compilar/instalar según tu entorno.

### 3) Variables de entorno

1. Copia la plantilla:

```bash
cp .env.example .env
```

2. Edita `.env` con tus valores.

Plantilla sugerida (sin espacios alrededor de `=`):

```dotenv
# PostgreSQL
DB_HOST=localhost
DB_NAME=089
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# ElevenLabs
ELEVENLABS_API_KEY=your_api_key
```

## Base de datos

El código asume que existen las tablas y restricciones necesarias. A continuación se muestra un **ejemplo mínimo** de esquema (ajústalo a tus necesidades):

```sql
CREATE TABLE IF NOT EXISTS agentes (
  id_agente TEXT PRIMARY KEY,
  nombre TEXT
);

CREATE TABLE IF NOT EXISTS conversaciones (
  id_conversacion BIGSERIAL PRIMARY KEY,
  id_eleven TEXT UNIQUE NOT NULL,
  id_agente TEXT,
  fecha DATE,
  hora_inicio TIME,
  hora_fin TIME,
  duracion TEXT,
  transcripcion TEXT,
  CONSTRAINT fk_agente
    FOREIGN KEY (id_agente) REFERENCES agentes(id_agente)
);

CREATE TABLE IF NOT EXISTS reportes (
  folio BIGSERIAL PRIMARY KEY,
  id_conversacion BIGINT UNIQUE NOT NULL,
  id_extorsion TEXT,
  modo TEXT,
  tiempo TEXT,
  lugar TEXT,
  CONSTRAINT fk_conversacion
    FOREIGN KEY (id_conversacion) REFERENCES conversaciones(id_conversacion)
);
```

## Uso

### Probar conexión a PostgreSQL

```bash
python db.py
```

### Sincronizar conversaciones (ElevenLabs → PostgreSQL)

```bash
python sync_conversations.py
```

Salida esperada (aprox.):

- “Iniciando sincronización de conversaciones…”
- Procesamiento por `conversation_id`
- Inserciones/actualizaciones en DB

## Notas importantes

- **Zona horaria:** el timestamp UNIX se convierte a `datetime` con la zona horaria local del servidor. Si tu fuente está en UTC, considera normalizar a UTC.
- **Transcripción y datos sensibles:** se almacena texto completo de la conversación. Define controles de acceso, retención y/o redacción.
- **Paginación/rate limits:** si ElevenLabs pagina resultados o limita peticiones, es posible que se requiera manejo adicional.

## 📝 Buenas prácticas Git

### Convenciones de commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```text
<tipo>(<scope opcional>): <descripción>

Tipos comunes:
- feat:     Nueva funcionalidad
- fix:      Corrección de bug
- docs:     Cambios en documentación
- style:    Formato (sin cambios de lógica)
- refactor: Reestructuración de código
- test:     Tests
- chore:    Mantenimiento
```

### Ejemplos

```bash
# ✅ Buenos commits
feat(db): agregar tabla de reportes
fix(sync): manejar conversación sin agent_id
docs(readme): documentar configuración de .env

# ❌ Malos commits
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "cambios varios"
```

### Workflow de ramas

```text
main     → Producción, siempre estable
develop  → Integración de features

feature/<nombre>  → Nueva funcionalidad
fix/<nombre>      → Corrección de bugs
docs/<nombre>     → Documentación
```

### Proceso de contribución

```bash
# 1) Crear rama desde develop
git checkout develop
git pull origin develop
git checkout -b feature/sync-improvements

# 2) Commits atómicos
git add sync_conversations.py
git commit -m "fix(sync): agregar timeout a requests"

# 3) Push y Pull Request
git push origin feature/sync-improvements
```
