# SIA Sync — Manual de Usuario Windows
### Universidad Nacional de Colombia

---

## Requisitos

- Windows 10 u 11
- Google Chrome instalado ([descargar aquí](https://www.google.com/chrome))
- Conexión a internet

> Instala Chrome antes de continuar. Sin Chrome la aplicación no puede conectarse al portal UNAL.

---

## 1. Instalación

### Paso 1 — Descargar

Descarga el archivo **IngresoNotas-Windows.zip** desde el enlace que te compartieron.

### Paso 2 — Descomprimir

Haz clic derecho sobre el ZIP → **Extraer todo** → **Extraer**.

Obtendrás una carpeta con el ejecutable de la aplicación.

### Paso 3 — Ejecutar

Haz doble clic en **app.exe**.

---

## 2. Primera apertura — Advertencia de seguridad

Windows puede mostrar una alerta de SmartScreen la primera vez:

1. Aparece la ventana **"Windows protegió tu PC"**.
2. Haz clic en **Más información**.
3. Luego haz clic en **Ejecutar de todas formas**.

> Solo necesitas hacer esto la primera vez.

Si el antivirus bloquea el archivo, agrégalo como excepción o desactiva temporalmente la protección en tiempo real para ejecutarlo.

---

## 3. Abrir la aplicación

Haz doble clic en **app.exe**.

Aparecerá una ventana de terminal — **no la cierres**, es el servidor de la aplicación. Unos segundos después el navegador se abrirá automáticamente en `http://127.0.0.1:5000`.

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

> No cierres el navegador ni la terminal durante el procesamiento.

---

### Paso 4 — Reporte de resultados

Al finalizar verás un reporte con:

| Indicador  | Descripción              |
|------------|--------------------------|
| Aprobados  | Nota ≥ 3.0               |
| Reprobados | Nota < 3.0               |
| Promedio   | Promedio del grupo       |
| Gráfica    | Distribución por rangos  |

Al final tienes dos opciones:
- **Sí, continuar** → procesar otro grupo en la misma sesión.
- **No, finalizar** → cerrar sesión.

---

## 5. Cerrar la aplicación

1. Haz clic en **No, finalizar** dentro de la app.
2. Cierra el navegador.
3. Cierra la ventana de terminal.

---

## 6. Solución de problemas

**Windows bloqueó el archivo y no aparece "Más información"**
Haz clic derecho sobre el `.exe` → **Propiedades** → marca **Desbloquear** al final de la ventana → **Aceptar**.

**El navegador no abre solo**
Escribe `http://127.0.0.1:5000` en el navegador manualmente.

**Error de credenciales**
Verifica usuario y contraseña en el portal SIA directamente. El usuario va sin `@unal.edu.co`.

**Chrome no encontrado**
Instala Google Chrome desde [google.com/chrome](https://www.google.com/chrome) y vuelve a intentar.

**El puerto 5000 está en uso**
Cierra cualquier otra instancia del programa. Si persiste, reinicia el computador e intenta de nuevo.

**La ventana de terminal aparece y desaparece inmediatamente**
Abre una terminal (CMD) manualmente y ejecuta el programa desde allí para ver el error:
```cmd
cd ruta\donde\está\app.exe
app.exe
```

---

*Sistema desarrollado para uso interno — Universidad Nacional de Colombia*
