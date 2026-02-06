# Backend-089
Archivos para la contrsuccion del backend del sistema del 089 para denuncias anónimas


## 📝 Buenas Prácticas Git

### Convenciones de commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):
```bash
(): 

# Tipos:
feat:     Nueva funcionalidad
fix:      Corrección de bug
docs:     Cambios en documentación
style:    Formateo, sin cambios de lógica
refactor: Reestructuración de código
test:     Tests
chore:    Mantenimiento
```

### Ejemplos
```bash
# ✅ Buenos commits
feat(db): agregar tabla de reportes
fix(api): resolver timeout en webhooks
docs(readme): actualizar guía de instalación
refactor(parser): extraer lógica de validación

# ❌ Malos commits
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "cambios varios"
```

### Workflow de ramas
```bash
# Rama principal
main  → Producción, siempre estable

# Rama de desarrollo
develop  → Integración de features

# Features
feature/nombre-feature  → Nueva funcionalidad
fix/nombre-bug          → Corrección de bugs
docs/nombre-doc         → Documentación
```

### Proceso de contribución
```bash
# 1. Crear rama desde develop
git checkout develop
git pull origin develop
git checkout -b feature/webhook-validation

# 2. Hacer commits atómicos
git add src/webhook.py
git commit -m "feat(webhook): agregar validación de firma"

# 3. Push y crear Pull Request
git push origin feature/webhook-validation

# 4. Después de aprobación, merge a develop
```
