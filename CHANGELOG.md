# Changelog - My Trello Clone

Este archivo documenta todos los cambios realizados en el proyecto.

---

## [2024-12-10] - Sesión de Mejoras Principales

### 🔐 1. Filtrado de Tableros por Usuario

**Problema:** Todos los usuarios veían los mismos tableros, sin importar quién los creó.

**Solución:**
- **Backend (`app/routes/boards.py`):** Se añadió autenticación obligatoria a todas las rutas.
- **Backend (`app/models/board.py`):** Nueva función `get_boards_by_user(db, user_id)` para filtrar tableros.
- **Frontend (`frontend/src/services/TableroService.js`):** Interceptor de axios que añade automáticamente el token de autenticación a todas las peticiones.

---

### 🎨 2. Creación de Tableros

**Problema:** 
1. Error 401 al crear tableros.
2. Los tableros nuevos no aparecían sin recargar la página.
3. El botón "Crear Tablero" no era visible.

**Solución:**
- **`BoardService.js`:** Se añadió el interceptor de autenticación.
- **`Cabecera.jsx`:** Después de crear un tablero, se navega directamente a él sin recargar.
- **`Cabecera.module.css`:** Estilos CSS para hacer visible el botón de submit.

---

### ✏️ 3. Edición y Eliminación de Tarjetas

**Características implementadas:**
- Modal con título editable
- Campo de descripción con textarea
- Botón "Guardar" para confirmar cambios
- Botón "Eliminar" con confirmación

**Archivos modificados:**
- `frontend/src/components/Card/Card.jsx` - UI del modal
- `frontend/src/components/Card/Card.module.css` - Estilos
- `frontend/src/services/TableroService.js` - Funciones `editarTarjeta` y `eliminarTarjeta`
- `frontend/src/hooks/useTablero.js` - Handlers `editarTarjetaHandler` y `eliminarTarjetaHandler`

---

### 📋 4. Edición y Eliminación de Columnas

**Características implementadas:**
- Título de columna clickeable para edición inline
- Menú de opciones (⋮) con dropdown
- Opción "Eliminar columna" con confirmación

**Archivos modificados:**
- `frontend/src/components/Columna/Columna.jsx` - UI de edición
- `frontend/src/components/Columna/TarjetaLista.module.css` - Estilos del menú
- `frontend/src/services/TableroService.js` - Funciones `editarColumna` y `eliminarColumna`
- `frontend/src/hooks/useTablero.js` - Handlers `editarColumnaHandler` y `eliminarColumnaHandler`

---

### 🐛 5. Corrección del Parpadeo del Modal (Flicker)

**Problema:** Al hacer clic en una tarjeta, el modal parpadeaba porque el evento de clic conflictuaba con el drag-and-drop.

**Solución:**
1. Se creó un `dragHandle` separado (ícono de arrastre) para los listeners de drag.
2. Se añadió `disabled: isModalOpen` al hook `useDraggable` para desactivar el arrastre mientras el modal está abierto.
3. Se usó `e.stopPropagation()` en los handlers de clic.

---

### 🖱️ 6. Mejora Visual del Drag and Drop

**Problema:** La tarjeta al arrastrar no tenía buen aspecto visual.

**Solución:**
- Se implementó `DragOverlay` de `@dnd-kit/core` para mostrar una preview estilizada.
- Estilos CSS con rotación, sombra y gradiente para una experiencia premium.

**Archivos modificados:**
- `frontend/src/components/Tablero/Tablero.jsx` - Implementación de `DragOverlay`
- `frontend/src/components/Tablero/Tablero.module.css` - Clase `.dragPreview`

---

### 🔧 7. Corrección de Bug en Drag and Drop

**Problema:** Error `undefined is not an object (evaluating 'card.id')` al arrastrar tarjetas.

**Causa:** La función `moverTarjeta` usaba `splice` que mutaba el array y dejaba elementos `undefined`.

**Solución:**
- Se refactorizó `moverTarjeta` para usar operaciones inmutables (`filter` y `map`).
- Se añadió filtro `(columna.cards || []).filter(c => c)` en `SortableContext`.

---

### 🚀 8. Modal con React Portal

**Mejora:** El componente `Modal` ahora usa `createPortal` para renderizarse fuera del árbol de `DndContext`, evitando interferencias con eventos de drag.

---

## Estructura de Archivos Modificados

```
backend/
├── app/
│   ├── models/
│   │   └── board.py          # get_boards_by_user, create_board con user_id
│   └── routes/
│       └── boards.py         # Autenticación en todas las rutas

frontend/src/
├── components/
│   ├── Cabecera/
│   │   ├── Cabecera.jsx      # Navegación después de crear tablero
│   │   └── Cabecera.module.css
│   ├── Card/
│   │   ├── Card.jsx          # Modal editable, drag handle
│   │   └── Card.module.css
│   ├── Columna/
│   │   ├── Columna.jsx       # Edición inline, menú opciones
│   │   └── TarjetaLista.module.css
│   ├── Tablero/
│   │   ├── Tablero.jsx       # DragOverlay, callbacks
│   │   └── Tablero.module.css
│   └── modal/
│       └── Modal.jsx         # React Portal
├── hooks/
│   ├── useBoardCabecera.js   # Callback onSuccess
│   ├── useTablero.js         # Handlers CRUD, moverTarjeta inmutable
│   └── useTableros.js        # Función refetch
└── services/
    ├── BoardService.js       # Interceptor auth
    └── TableroService.js     # Funciones CRUD completas
```

---

## Dependencias Utilizadas

| Dependencia | Uso |
|-------------|-----|
| `axios` | Peticiones HTTP con interceptores |
| `@dnd-kit/core` | Drag and drop base |
| `@dnd-kit/sortable` | Ordenamiento de tarjetas |
| `react-router-dom` | Navegación programática |
| `react-markdown` | Pendiente: renderizado de markdown |

---

## Próximos Pasos Sugeridos

- [ ] Implementar renderizado de Markdown en la descripción de tarjetas
- [ ] Añadir fechas de vencimiento a las tarjetas
- [ ] Implementar etiquetas/labels con colores
- [ ] Añadir asignación de usuarios a tarjetas
- [ ] Implementar búsqueda de tarjetas
