# Buenas Prácticas Git - Guía del Equipo

## 📋 Convenciones de Commits

### Estructura básica

```
<tipo>(<alcance>): <descripción corta>

<cuerpo opcional: explicación detallada>

<footer opcional: referencias, breaking changes>
```

---

## 🏷️ Tipos de Commit

|    Tipo    |               Cuándo usarlo              |                   Ejemplo                 |
|------------|------------------------------------------|-------------------------------------------|
| `feat`     | Nueva funcionalidad                      | `feat(api): agregar endpoint de reportes` |
| `fix`      | Corrección de bug                        | `fix(db): resolver timeout en conexión`   |
| `docs`     | Documentación                            | `docs(readme): actualizar instrucciones`  |
| `style`    | Formateo de código                       | `style: aplicar black formatter`          |
| `refactor` | Reestructuración sin cambios funcionales | `refactor(parser): extraer validaciones`  |
| `test`     | Tests                                    | `test(api): agregar tests de integración` |
| `chore`    | Mantenimiento                            | `chore(deps): actualizar dependencias`    |
| `perf`     | Optimización                             | `perf(query): optimizar consulta SQL`     |

---

## ✅ Reglas de Oro

### 1. Usa imperativo (como dar órdenes)

```bash
✅ feat(auth): add login endpoint
✅ fix(db): resolve connection timeout
✅ docs(api): update webhook documentation

❌ feat(auth): added login endpoint
❌ fix(db): fixed connection timeout
❌ docs(api): updating webhook documentation
```

### 2. Primera línea: máximo 50-72 caracteres

```bash
✅ fix(webhook): resolver error de parsing JSON
❌ fix(webhook): resolver el problema de parsing de JSON que ocurría cuando los datos venían mal formateados desde ElevenLabs
```

### 3. Sin punto final en la descripción

```bash
✅ feat(api): agregar validación de schemas
❌ feat(api): agregar validación de schemas.
```

### 4. Separa el cuerpo con línea en blanco

```bash
✅
feat(email): implementar notificaciones

Se agrega servicio de email con plantillas
usando SendGrid. Incluye retry logic.

❌
feat(email): implementar notificaciones. Se agrega servicio de email...
```

---

## 🎯 Commits Atómicos

### ❌ Mal - Un commit hace muchas cosas:

```bash
git commit -m "fix bugs, add feature, update docs"
```

### ✅ Bien - Un commit por cambio lógico:

```bash
git commit -m "fix(auth): resolver validación de tokens"
git commit -m "feat(user): agregar endpoint de perfil"
git commit -m "docs(api): documentar nuevos endpoints"
```

**¿Por qué?**
- Más fácil de revisar
- Más fácil de revertir si algo falla
- Mejor historial
- Facilita cherry-pick

---

## 📝 Ejemplos Prácticos

### Ejemplo 1: Feature simple

```bash
feat(webhook): agregar validación de firma
```

### Ejemplo 2: Feature con explicación

```bash
feat(cache): implementar caché con Redis

Las consultas a /conversations estaban tomando 2-3 segundos.
Se implementa caché de 5 minutos, reduciendo el tiempo a ~50ms.

Closes #123
```

### Ejemplo 3: Bug fix

```bash
fix(db): usar Connection Pooler en lugar de conexión directa

Resuelve el error "server closed the connection unexpectedly"
usando el pooler de Supabase en puerto 6543.

Fixes #456
```

### Ejemplo 4: Refactoring

```bash
refactor(parser): extraer lógica de validación a función separada

Se extrae validate_conversation_data() para mejorar legibilidad
y facilitar testing unitario.
```

### Ejemplo 5: Breaking change

```bash
feat(api)!: cambiar formato de respuesta del webhook

BREAKING CHANGE: el webhook ahora retorna {status, data, errors}
en lugar de {success, result}

Migración:
- Cambiar response.success por response.status
- Cambiar response.result por response.data
```

---

## 🔧 Alcance (Scope)

El alcance indica qué parte del código se modificó:

```bash
# Por módulo/componente
feat(auth): implementar login con JWT
fix(webhook): corregir manejo de errores

# Por archivo/clase
refactor(DatabaseManager): optimizar conexiones
style(ElevenLabsExtractor): aplicar formateo

# Por funcionalidad
feat(reports): agregar filtro por fecha
fix(api): resolver timeout en requests
```

---

### Ejemplo completo

```bash
feat(api): migrar autenticación a OAuth2

BREAKING CHANGE: Se elimina autenticación básica.
Todos los clientes deben migrar a OAuth2.

Pasos de migración:
1. Obtener client_id y client_secret
2. Actualizar headers: Authorization: Bearer <token>

Closes #234
Co-authored-by: María García <maria@ejemplo.com>
```

---

## 🚫 Errores Comunes

|      ❌ No hacer       |                 ✅ Hacer                  |
|------------------------|--------------------------------------------|
| `fix stuff`            | `fix(auth): resolver validación de tokens` |
| `WIP`                  | `feat(api): agregar endpoint users (WIP)`  |
| `asdfasdf`             | ❌ Nunca                                   |
| `Fixed bug`            | `fix(parser): resolver error con null`     |
| `Updated files`        | `docs(readme): actualizar instalación`     |
| Commits de 50 archivos | Commits atómicos                           |

---

## 📦 Workflow de Trabajo

### 1. Antes de empezar

```bash
# Actualizar rama principal
git checkout develop
git pull origin develop

# Crear rama para tu feature
git checkout -b feature/nombre-descriptivo
```

### 2. Durante el desarrollo

```bash
# Ver qué cambios tienes
git status
git diff

# Agregar solo archivos relacionados
git add src/auth.py tests/test_auth.py

# Commit con mensaje claro
git commit -m "feat(auth): implementar login con JWT"
```

### 3. Múltiples commits relacionados

```bash
# Primera funcionalidad
git add src/database.py
git commit -m "feat(db): agregar tabla de usuarios"

# Tests para esa funcionalidad
git add tests/test_database.py
git commit -m "test(db): agregar tests para tabla usuarios"

# Documentación
git add docs/database.md
git commit -m "docs(db): documentar schema de usuarios"
```

### 4. Antes de hacer push

```bash
# Revisar historial
git log --oneline

# Ver diferencias con develop
git diff develop

# Push de tu rama
git push origin feature/nombre-descriptivo
```

---

## 🌿 Estrategia de Ramas

### Ramas principales

```bash
main       → Producción (siempre estable)
develop    → Integración de features
```

### Ramas de trabajo

```bash
feature/nombre    → Nueva funcionalidad
fix/nombre        → Corrección de bugs
docs/nombre       → Documentación
refactor/nombre   → Refactoring
```

### Ejemplo de flujo

```bash
# Crear feature
git checkout develop
git checkout -b feature/webhook-validation

# Desarrollar (varios commits)
git commit -m "feat(webhook): agregar schema de validación"
git commit -m "test(webhook): agregar tests de validación"
git commit -m "docs(webhook): documentar endpoint"

# Push y crear Pull Request
git push origin feature/webhook-validation

# Después de revisión y aprobación
# Se hace merge a develop (por GitHub/GitLab)

# Eventualmente develop se mergea a main para deploy
```

---

## 🔍 Revisión de Código

### Antes de crear Pull Request

- [ ] El código compila sin errores
- [ ] Los tests pasan (`pytest tests/`)
- [ ] Código formateado (`black .`)
- [ ] Sin warnings de linting
- [ ] Commits siguen convenciones
- [ ] No hay claves/passwords en el código
- [ ] README actualizado si es necesario

### Al revisar PR de otros

- ✅ Revisa la lógica, no solo la sintaxis
- ✅ Verifica que los tests sean suficientes
- ✅ Comenta de forma constructiva
- ✅ Aprueba solo si está listo para producción

---

## 🛠️ Herramientas Útiles

### Configurar template de commit

Crea `.gitmessage` en tu home:

```
# <tipo>(<alcance>): <descripción>
# |<----  Máximo 50 caracteres  ---->|

# Explicación (opcional)
# |<----  Máximo 72 caracteres  ---->|

# Footer (opcional)
# Closes #
# BREAKING CHANGE:

# --- Tipos ---
# feat: Nueva funcionalidad
# fix: Corrección de bug
# docs: Documentación
# refactor: Refactoring
# test: Tests
# chore: Mantenimiento
```

Actívalo:

```bash
git config --global commit.template ~/.gitmessage
```

### Alias útiles

```bash
# Ver log bonito
git config --global alias.lg "log --graph --oneline --all --decorate"

# Ver últimos 10 commits
git config --global alias.last "log -10 --oneline"

# Ver cambios por autor
git config --global alias.mine "log --author='TuNombre'"
```

Úsalos:

```bash
git lg
git last
git mine
```

---

## 📚 Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Semantic Versioning](https://semver.org/)

---

## ❓ FAQ

### ¿Cuándo hacer commit?

✅ Haz commit cuando:
- Completes una funcionalidad pequeña y funcional
- Arregles un bug específico
- Hagas un refactor autocontenido
- Termines un test

❌ NO hagas commit cuando:
- El código no compile
- Los tests estén rotos
- Hayas mezclado múltiples cambios

### ¿Qué tan grande debe ser un commit?

**Regla de oro:** Si no puedes describir el commit en una línea clara, probablemente es muy grande.

### ¿Puedo editar commits ya hechos?

```bash
# Editar el último commit
git commit --amend

# Editar varios commits (SOLO si NO has hecho push)
git rebase -i HEAD~3

# ⚠️ NO edites commits que ya están en remoto (después de push)
```

### ¿Qué hago si me equivoqué en el mensaje?

```bash
# Si NO has hecho push
git commit --amend -m "feat(api): mensaje corregido"

# Si YA hiciste push
# Deja el mensaje como está o contacta al líder del equipo
```

---

**Última actualización:** 2024-02-06  
**Mantenido por:** Equipo DOTI

Prueba del pull request