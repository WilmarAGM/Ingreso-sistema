# SIA Sync — Manual de Uso
### Universidad Nacional de Colombia

---

## Requisitos previos

| Requisito | Linux | Mac |
|---|---|---|
| Google Chrome o Chromium | Requerido (el instalador lo gestiona) | Requerido (instalar manualmente desde [google.com/chrome](https://www.google.com/chrome)) |
| ChromeDriver | Requerido (el instalador lo gestiona) | Se instala automáticamente con Chrome |
| Conexión a internet | Requerido | Requerido |

---

## 1. Instalación

### Linux

1. Descarga el archivo **IngresoNotas-Linux.zip** desde los releases del proyecto.
2. Descomprime el ZIP. Obtendrás una carpeta con:
   ```
   IngresoNotas-Linux/
   ├── IngresoNotas.app/   ← el programa
   └── instalar.sh         ← el instalador
   ```
3. Abre una terminal dentro de la carpeta y ejecuta:
   ```bash
   bash instalar.sh
   ```
4. El instalador verificará Chrome/Chromium, copiará la aplicación y creará un acceso directo en el escritorio.

> Si el sistema pide contraseña de administrador durante la instalación, es para instalar Chrome automáticamente.

### Mac

1. Descarga el archivo **IngresoNotas-Mac.zip** desde los releases del proyecto.
2. Descomprime el ZIP. Obtendrás:
   ```
   IngresoNotas-Mac/
   ├── IngresoNotas.app   ← la aplicación
   └── instalar.dmg       ← imagen de disco
   ```
3. Abre **instalar.dmg** haciendo doble clic.
4. Arrastra **IngresoNotas.app** a la carpeta **Applications** que aparece en la ventana.
5. Cierra la imagen de disco y expúlsala.

> **Primera apertura en Mac:** el sistema puede mostrar una alerta de seguridad. Ve a  
> **Ajustes del Sistema → Privacidad y Seguridad → Abrir de todas formas.**

---

## 2. Iniciar la aplicación

### Linux
- Haz doble clic en el icono **Ingreso de Notas** del escritorio, **o**
- Ejecuta en terminal: `ingreso-notas`

### Mac
- Abre **Launchpad** y busca **IngresoNotas**, **o**
- Ve a **Aplicaciones** y haz doble clic en **IngresoNotas.app**

Después de unos segundos, el navegador se abrirá automáticamente en `http://127.0.0.1:5000`.

> En Linux aparecerá una ventana de terminal: **no la cierres**, ya que es el servidor de la aplicación.

---

## 3. Flujo de uso paso a paso

### Paso 1 — Inicio de sesión

1. En el campo **Usuario** escribe tu usuario institucional (sin `@unal.edu.co`).
   - Ejemplo: si tu correo es `wamartinezg@unal.edu.co`, escribe `wamartinezg`
2. Ingresa tu **contraseña** del SIA.
3. Haz clic en **Continuar**.

El sistema se conectará automáticamente al portal de autenticación de la UNAL. Este proceso puede tardar entre 15 y 30 segundos.

> Si las credenciales son incorrectas, aparecerá un mensaje de error en rojo con una captura de pantalla del portal para ayudarte a diagnosticar el problema.

---

### Paso 2 — Selección de grupo

1. En el menú desplegable aparecerán todos tus grupos académicos del período actual.
2. Selecciona el grupo al que quieres ingresar notas.
3. Espera a que el sistema sincronice las evaluaciones disponibles (indicador "Sincronizando con SIA...").
4. Haz clic en **Siguiente: Cargar archivo**.

---

### Paso 3 — Cargar archivo y mapear columnas

#### 3.1 Preparar el archivo Excel

El archivo debe tener:
- Una columna llamada exactamente **Documento** con el número de identificación de cada estudiante.
- Una o más columnas numéricas con las notas de cada evaluación.

Ejemplo de estructura válida:

| Documento | Parcial 1 | Parcial 2 | Final |
|---|---|---|---|
| 1020456789 | 3.8 | 4.2 | 3.5 |
| 1045123456 | 2.7 | 3.1 | 3.9 |

Formatos aceptados: `.xlsx`, `.xls`, `.xlsm`, `.csv`

#### 3.2 Subir el archivo

1. Haz clic en el área punteada **"Selecciona tu archivo de notas"**.
2. Elige el archivo desde tu computador.

#### 3.3 Enlazar evaluaciones

Después de cargar el archivo aparecerá el panel de **Enlace de evaluaciones**:

- La columna izquierda muestra las evaluaciones registradas en el SIA para ese grupo.
- La columna derecha muestra un menú con las columnas numéricas de tu Excel.
- Selecciona qué columna del Excel corresponde a cada evaluación del SIA.
- Si una evaluación no la vas a ingresar en esta sesión, déjala en **— Ignorar —**.

#### 3.4 Iniciar el procesamiento

1. Haz clic en **Iniciar procesamiento**.
2. El panel de progreso mostrará en tiempo real los pasos del bot:
   - Selección de evaluación en el SIA
   - Página por página de estudiantes
   - Guardado automático tras cada página
3. Espera hasta que el sistema indique **¡PROCESO MULTI-NOTA FINALIZADO!**

> No cierres el navegador ni la aplicación durante el procesamiento.

---

### Paso 4 — Reporte de resultados

Al finalizar, la aplicación muestra un reporte por cada evaluación procesada:

| Indicador | Descripción |
|---|---|
| **Aprobados** | Estudiantes con nota ≥ 3.0 |
| **Reprobados** | Estudiantes con nota < 3.0 |
| **Promedio** | Promedio del grupo para esa evaluación |
| **Gráfica de barras** | Distribución de notas por rangos [0,1) [1,2) [2,3) [3,4) [4,5] |

Al final del reporte tienes dos opciones:

- **Sí, continuar** → vuelve a la selección de grupos para procesar otro grupo en la misma sesión.
- **No, finalizar** → cierra la sesión correctamente.

---

## 4. Cerrar la aplicación

1. Haz clic en **No, finalizar** dentro de la app (recomendado) para cerrar la sesión del SIA correctamente.
2. Luego cierra el navegador.
3. En Linux: cierra la ventana de terminal que se abrió al iniciar.  
   En Mac: la aplicación se cerrará sola al terminar la sesión.

---

## 5. Preguntas frecuentes

**¿Por qué tarda en conectarse al iniciar sesión?**  
El bot abre Chrome en modo oculto y navega por el portal UNAL. El proceso normal toma entre 15 y 30 segundos.

**¿Qué pasa si hay un error durante el ingreso de notas?**  
El bot registra el error en el log en tiempo real y continúa con la siguiente página. Al finalizar puedes revisar qué notas no se procesaron en el log.

**¿Puedo ingresar notas de varias evaluaciones al mismo tiempo?**  
Sí. En el paso 3 puedes enlazar varias columnas de tu Excel con varias evaluaciones del SIA. El bot las procesará una por una de forma automática.

**¿El programa guarda mis credenciales?**  
No. Las credenciales solo se usan durante la sesión activa y nunca se almacenan en disco.

**El navegador se abre pero la página no carga.**  
Espera 5 segundos y recarga la página (`F5`). Si persiste, cierra y vuelve a abrir la aplicación.

**En Mac aparece "La app no puede abrirse porque proviene de un desarrollador no identificado".**  
Ve a **Ajustes del Sistema → Privacidad y Seguridad** y haz clic en **Abrir de todas formas** junto al nombre de la aplicación.

---

## 6. Soporte

Para reportar errores o solicitar ayuda, contacta al equipo de desarrollo a través del repositorio del proyecto.
