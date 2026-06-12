# SIA Sync — Manual de Usuario Linux
### Universidad Nacional de Colombia

---

## Requisitos

- Sistema operativo Linux (Ubuntu 20.04 o superior recomendado)
- Google Chrome o Chromium instalado
- Conexión a internet

---

## 1. Instalación

### Paso 1 — Descargar

Descarga el archivo **IngresoNotas-Linux.zip** desde el enlace que te compartieron.

### Paso 2 — Descomprimir

Haz clic derecho sobre el ZIP y selecciona **Extraer aquí**, o desde la terminal:

```bash
unzip IngresoNotas-Linux.zip
```

Obtendrás una carpeta con esta estructura:

```
IngresoNotas-Linux/
├── IngresoNotas.app/   ← el programa
└── instalar.sh         ← el instalador
```

### Paso 3 — Ejecutar el instalador

Abre una terminal dentro de la carpeta `IngresoNotas-Linux` y ejecuta:

```bash
bash instalar.sh
```

El instalador:
- Verifica que Chrome o Chromium esté instalado (lo instala automáticamente si falta)
- Copia el programa a tu carpeta de usuario
- Crea un ícono **Ingreso de Notas** en el escritorio

> Si el sistema pide tu contraseña durante la instalación, es para instalar Chrome. Es normal.

---

## 2. Abrir la aplicación

Haz doble clic en el ícono **Ingreso de Notas** del escritorio.

Aparecerá una ventana de terminal — **no la cierres**, es el servidor de la aplicación. Unos segundos después el navegador se abrirá automáticamente en `http://127.0.0.1:5000`.

> Si el navegador no abre solo, escribe manualmente `http://127.0.0.1:5000` en la barra de direcciones.

---

## 3. Uso paso a paso

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

> No cierres el navegador ni la terminal durante el procesamiento.

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

## 4. Cerrar la aplicación

1. Haz clic en **No, finalizar** dentro de la app.
2. Cierra el navegador.
3. Cierra la ventana de terminal.

---

## 5. Solución de problemas

**El navegador no abre solo**
Escribe `http://127.0.0.1:5000` en el navegador manualmente.

**Error de credenciales**
Verifica usuario y contraseña en el portal SIA directamente. El usuario va sin `@unal.edu.co`.

**La terminal se cierra sola al abrir la app**
Abre la app desde la terminal manualmente:
```bash
~/.local/share/IngresoNotas/IngresoNotas
```

**El puerto 5000 está en uso**
Cierra cualquier otra instancia del programa y vuelve a intentar.

---

*Sistema desarrollado para uso interno — Universidad Nacional de Colombia*
