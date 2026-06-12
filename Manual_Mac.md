# SIA Sync — Manual de Usuario macOS
### Universidad Nacional de Colombia

---

## Requisitos

- macOS 11 Big Sur o superior
- Google Chrome instalado ([descargar aquí](https://www.google.com/chrome))
- Conexión a internet

> Instala Chrome antes de continuar. Sin Chrome la aplicación no puede conectarse al portal UNAL.

---

## 1. Instalación

### Paso 1 — Descargar

Descarga el archivo **IngresoNotas-Mac.zip** desde el enlace que te compartieron.

### Paso 2 — Descomprimir

Haz doble clic sobre el ZIP. Obtendrás una carpeta con:

```
IngresoNotas-Mac/
├── IngresoNotas.app   ← la aplicación
└── instalar.dmg       ← imagen de disco para instalar
```

### Paso 3 — Instalar desde el DMG

1. Haz doble clic en **instalar.dmg**.
2. Se abrirá una ventana con la aplicación y una flecha hacia la carpeta **Applications**.
3. Arrastra **IngresoNotas.app** sobre la carpeta **Applications**.
4. Espera que termine de copiarse.
5. Cierra la ventana y expulsa el disco (clic derecho → Expulsar).

---

## 2. Primera apertura — Permiso de seguridad

macOS bloquea aplicaciones de desarrolladores no registrados. Para abrirla la primera vez:

**Opción A — Desde Finder:**
1. Ve a la carpeta **Aplicaciones**.
2. Haz **clic derecho** sobre **IngresoNotas** → **Abrir**.
3. En la alerta que aparece haz clic en **Abrir** nuevamente.

**Opción B — Desde Ajustes del Sistema:**
1. Intenta abrir la app normalmente; aparecerá la alerta de bloqueo.
2. Ve a **Ajustes del Sistema → Privacidad y Seguridad**.
3. Baja hasta encontrar el mensaje sobre IngresoNotas y haz clic en **Abrir de todas formas**.

> Solo necesitas hacer esto la primera vez. Después abre normalmente.

---

## 3. Abrir la aplicación

Haz doble clic en **IngresoNotas** desde Launchpad o desde la carpeta Aplicaciones.

Unos segundos después el navegador se abrirá automáticamente en `http://127.0.0.1:5000`.

> Si el navegador no abre solo, escribe manualmente `http://127.0.0.1:5000` en la barra de direcciones.

---

## 4. Uso paso a paso

### Paso 1 — Iniciar sesión

1. En el campo **Usuario** escribe tu usuario institucional **sin** `@unal.edu.co`.

   Ejemplo: si tu correo es `wamartinezg@unal.edu.co` → escribe `wamartinezg`

2. Escribe tu **contraseña** del SIA.
3. Haz clic en **Continuar**.

El sistema se conecta automáticamente al portal UNAL. Espera entre 15 y 30 segundos.

> Si las credenciales son incorrectas aparecerá un mensaje en rojo con una captura del portal.

---

### Paso 2 — Seleccionar grupo

1. Elige tu grupo académico en el menú desplegable.
2. Espera que aparezca el mensaje **"Sincronizando con SIA..."** y desaparezca.
3. Haz clic en **Siguiente: Cargar archivo**.

---

### Paso 3 — Cargar el archivo y mapear columnas

#### Preparar el archivo Excel

Tu archivo debe tener:

- Una columna llamada exactamente **Documento** con el número de identificación de cada estudiante.
- Una o más columnas numéricas con las notas.

| Documento  | Parcial 1 | Parcial 2 | Final |
|------------|-----------|-----------|-------|
| 1020456789 | 3.8       | 4.2       | 3.5   |
| 1045123456 | 2.7       | 3.1       | 3.9   |

Formatos aceptados: `.xlsx` `.xls` `.xlsm` `.csv`

#### Subir el archivo

Haz clic en el área punteada y selecciona tu archivo.

#### Enlazar evaluaciones

- Columna izquierda: evaluaciones registradas en el SIA para ese grupo.
- Columna derecha: columnas de tu Excel.
- Selecciona qué columna corresponde a cada evaluación.
- Si no vas a ingresar una evaluación, déjala en **— Ignorar —**.

#### Iniciar

Haz clic en **Iniciar procesamiento** y espera. El log en pantalla muestra el avance en tiempo real.

> No cierres el navegador durante el procesamiento.

---

### Paso 4 — Reporte de resultados

Al finalizar verás un reporte con:

| Indicador | Descripción |
|-----------|-------------|
| Aprobados | Nota ≥ 3.0 |
| Reprobados | Nota < 3.0 |
| Promedio | Promedio del grupo |
| Gráfica | Distribución por rangos |

Al final tienes dos opciones:
- **Sí, continuar** → procesar otro grupo en la misma sesión.
- **No, finalizar** → cerrar sesión.

---

## 5. Cerrar la aplicación

1. Haz clic en **No, finalizar** dentro de la app.
2. Cierra el navegador.
3. La aplicación se cierra sola.

---

## 6. Solución de problemas

**"La app no puede abrirse porque proviene de un desarrollador no identificado"**
Sigue los pasos de la sección 2 (Primera apertura).

**El navegador no abre solo**
Escribe `http://127.0.0.1:5000` en el navegador manualmente.

**Error de credenciales**
Verifica usuario y contraseña en el portal SIA directamente. El usuario va sin `@unal.edu.co`.

**Chrome no encontrado**
Instala Google Chrome desde [google.com/chrome](https://www.google.com/chrome) y vuelve a intentar.

**La app se abre y cierra inmediatamente**
Abre la app desde Terminal para ver el error:
```bash
/Applications/IngresoNotas.app/Contents/MacOS/IngresoNotas
```

---

*Sistema desarrollado para uso interno — Universidad Nacional de Colombia*
