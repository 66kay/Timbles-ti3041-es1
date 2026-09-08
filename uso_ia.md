# Documento de uso de IA

## Parte 1: Registro de consultas

A continuación se detallan las consultas (prompts) realizadas a la IA durante el desarrollo de la Evaluación Sumativa 1, junto con un resumen de sus respuestas y cómo se integraron al proyecto.

### Consulta 1
**Prompt Textual:** "porque me da error" / "pq me da error" (Refiriéndose a la instalación inicial del entorno virtual y comandos base).
**Respuesta de la IA:** La IA explicó la sintaxis correcta para instalar Django en Windows y sugirió los comandos correctos para iniciar el proyecto.
**Qué se usó o modificó:** Se utilizaron las correcciones sugeridas para configurar el entorno virtual e instalar Django correctamente (Etapa 0).

### Consulta 2
**Prompt Textual:** "analiza bien el proyecto para que tengas claro lo que haremos y me guiaras paso a paso en cada cosa que me pidan en los requerimientos del 1 al 1.1.4"
**Respuesta de la IA:** La IA analizó los requerimientos (rúbrica) y generó un plan de acción estructurado desde la Etapa 0 hasta la Etapa 3.
**Qué se usó o modificó:** Se utilizó esta respuesta para tener una hoja de ruta clara sobre qué tareas de programación correspondían a cada punto exigido en la pauta.

### Consulta 3
**Prompt Textual:** "dame el comando para crear o empezar con la etapa 1 y guiame paso a paso para la creacion de las cosas"
**Respuesta de la IA:** La IA entregó las directrices iniciales y los comandos de creación de la aplicación.
**Qué se usó o modificó:** Se utilizaron los comandos iniciales sugeridos por la IA para crear la app `catalogo`. Sin embargo, el código de las vistas, el registro de la app en `settings.py` y la configuración de las URLs (Etapa 1) se realizó de forma manual basándose en lo aprendido en clases; la IA solo se usó para ahorrar tiempo con algunos comandos básicos en consola.

### Consulta 4
**Prompt Textual:** "usaremos la ferreteria. asi que paso a paso me ayudaras a crear las cosas y me crearas y documentaras todo para ir completando las cosas paso a paso"
**Respuesta de la IA:** La IA generó un archivo `productos.json` con 40 registros simulados. Posteriormente, apoyó indicando cómo construir la vista para leer el archivo y cómo conectar el diseño usando herencia de templates (`base.html`, `lista.html`, `detalle.html`).
**Qué se usó o modificó:** Se integró el archivo JSON directamente, y se usaron las explicaciones de la IA para estructurar correctamente el código HTML y las vistas de Django solicitadas en la Etapa 2.

### Consulta 5
**Prompt Textual:** "ahora me explicaras paso a paso que hacer en a etapa 3"
**Respuesta de la IA:** La IA explicó cómo calcular el total matemático del stock en Python y cómo escribir los condicionales en HTML (`{% if %}`) para pintar las filas agotadas de rojo.
**Qué se usó o modificó:** Se adaptó la lógica matemática propuesta por la IA en el archivo `views.py` y se aplicaron las reglas visuales al archivo `lista.html` para cumplir con la Etapa 3.

---

## Parte 2: Explicación del proceso

> [!WARNING]
> IMPORTANTE: Borra este recuadro de advertencia antes de entregar. Redacta a continuación tu experiencia personal con tus propias palabras.

*(Escribe aquí entre 10 y 20 líneas en total respondiendo libremente a lo siguiente:)*

1. **¿Cómo usaste a la IA?** *(Ejemplo: Empecé pidiéndole ayuda para configurar el entorno porque no recordaba los comandos, luego le pasé la pauta...)*
2. **¿Qué le pediste y por qué?** *(Ejemplo: Le pedí que me generara los datos del JSON porque inventar 40 productos a mano tomaba mucho tiempo...)*
3. **¿Qué respuestas te sirvieron tal cual y cuáles tuviste que corregir?** *(Ejemplo: El archivo de datos JSON me sirvió perfectamente, pero en la Etapa 1 preferí hacer el código yo mismo guiándome por lo del instituto...)*
4. **¿Qué aprendiste en el proceso?** *(Ejemplo: Aprendí cómo pasar variables matemáticas desde Python a una página HTML y cómo usar herencia para no repetir código...)*
