---
description: Regla obligatoria para proyectos nuevos
globs: ["**/*"]
alwaysApply: true
---

# Regla: Workflow para Proyectos Nuevos

## OBLIGATORIO: Primer Paso para Cualquier Proyecto Nuevo

Cuando el usuario solicite crear un **proyecto nuevo**, **aplicacion nueva**, o **iniciar un nuevo desarrollo**, SIEMPRE seguir este orden:

### Paso 1: Verificar existencia de CLAUDE.md
- Si NO existe CLAUDE.md en el directorio del proyecto -> Ejecutar `/flow-md-architect create`
- Si existe CLAUDE.md -> Verificar que este completo con `/flow-md-architect audit`

### Paso 2: Solo despues de CLAUDE.md valido
- Proceder con `/flow-plan` para planificacion
- Luego `/flow-issue-create` para crear issues
- Finalmente `/flow-feature-build` para implementar

### Razon
CLAUDE.md es la "Constitucion" del proyecto. Sin este archivo:
- Los agentes no conocen el stack tecnologico
- No se puede determinar la metodologia (TDD/RAD/Standard)
- El core_team de agentes no esta definido
- Las validaciones de coherencia fallaran

**NUNCA saltar directamente a disenar arquitectura o planificar features sin CLAUDE.md.**
