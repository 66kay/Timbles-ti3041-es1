# Documento de uso de IA

## Parte 1: Prompts y Respuestas

## Consulta 1
**Prompt Textual:** porque me da error de instalacion del entorno virtual de django.  
**Respuesta de la IA:** La IA explico los comandos correctos que tenia que escribir y me dio las instrucciones para poder instalar Django correctamente (Etapa 0).  
**Que se uso o modifico:** Se modifico los comandos que utilice y termino funcionando.

## Consulta 2
**Prompt Textual:** analiza bien el proyecto para que tengas claro lo que haremos y me guiaras paso a paso en cada cosa que me pidan en los requerimientos del 1 al 1.1.4 para ayudarme a entender mejor el proyecto  
**Respuesta de la IA:** La IA analizo los requerimientos (rubrica) y genero un plan de accion estructurado desde la Etapa 0 hasta la Etapa 3 para ayudarme a entender el proyecto y generar las cosas mas directas posible y sin tantas vueltas.  
**Que se uso o modifico:** Se utilizo esta respuesta para tener una hoja de ruta clara sobre que tareas de programacion correspondian a cada punto exigido en la pauta y me genero un task para seguir las cosas necesarias.

## Consulta 3
**Prompt Textual:** dame la forma de iniciar con el proyecto para que todo este claro y poder avanzar con la etapa 0 y continuar con las siguientes  
**Respuesta de la IA:** La IA entrego las directrices iniciales y los comandos de creacion de la aplicacion.  
**Que se uso o modifico:** Se utilizaron los comandos iniciales sugeridos por la IA para crear la app catalogo. Sin embargo, el codigo de las vistas, el registro de la app en settings.py y la configuracion de las URLs (Etapa 1) se realizo de forma manual basandose en lo aprendido en clases, solo use a la IA para ahorrar tiempo con algunos comandos basicos en consola.

## Consulta 4
**Prompt Textual:** usaremos la ferreteria. ten claro las cosas necesarias para que me ayudes a crear y generes los productos o cosas necesarias para esta etapa 2 y ahorrar un poco de tiempo  
**Respuesta de la IA:** La IA me genero un archivo productos.json con 40 registros. Posteriormente, apoyo indicando como construir la vista para leer el archivo y como conectar el diseño usando herencia de templates (base.html, lista.html, detalle.html).  
**Que se uso o modifico:** Se integro el archivo JSON directamente, y se usaron las explicaciones de la IA para estructurar correctamente el codigo HTML y las vistas de Django solicitadas en la Etapa 2.

## Consulta 5
**Prompt Textual:** ahora me explicaras paso a paso que hacer en a etapa 3 y ademas me dejaras el task para ir biendo lo que me falta completar y ademas me crearas las ecuaciones o cosas matematicas necesarias para agilizar el tiempo  
**Respuesta de la IA:** La IA explico como calcular el total matematico del stock en Python y como escribir los condicionales en HTML (`{% if %}`) para imprimir las filas agotadas de rojo.  
**Que se uso o modifico:** Se adapto la logica matematica propuesta por la IA en el archivo views.py y se aplicaron las reglas visuales al archivo lista.html para cumplir con la Etapa 3.

## Consulta 6
**Prompt Textual:** hazme un login el cual funcione con user:admin y psswd:admin y tambien un user:cliente y contraseña:cliente y que solo el admin pueda editar o eliminar productos. deja todo ordenado y limpio y que todo se vea bonito
**Respuesta de la IA:** La IA me explico como hacer que el login funcione con el usuario y contraseña admin y cliente. Ademas, me explico como hacer que el carrito funcione descontando el stock.
**Que se uso o modifico:** Se utilizo el codigo generado por la IA para crear el login.html y la vista login_view.

## Consulta 7
**Prompt Textual:** necesito que modifiques todo y hagas una ferreteria en forma de tienda. que la persona tenga que logearse y haya un admin. pero solamente usaremos el admin admin, necesito que solamente hagas la parte front end buscando fotos realistas de todos los productos y dejando bonito la interfaz. ademas agregaras un logo y un carrito el cual al apretar puedas comprar directamente y cuando se compre se descontara el stock para que yo pueda hacer funcionar el Back end.  
**Respuesta de la IA:** La IA estructuro la landing page publica, la logica de sesiones para roles de usuario y administrador, la gestion del carrito con descuento automatico en el JSON y las rutas para modificar stock y eliminar productos, asi todo queda bien hecho y ahorrariamos tiempo de frontend.  
**Que se uso o modifico:** Se integro la navegacion completa en HTML y Django sin base de datos, separando los permisos para que solo el admin pueda editar o borrar registros del catalogo, se agregaron las rutas para que el admin pueda editar o borrar productos, ademas separamos las rutas de admin y las rutas de publico para que no se esten mezclando y se ve bien ordenado y un cliente no tenga privilegios de admin.

## Consulta 8
**Prompt Textual:** landing page, inicio de sesion como usuario y administrador (admin,admin) todo tiene que ser html. pseudo compras, el stock se tiene que descontar y si no hay mas productos aparezca pero sin stock, que el usuario tenga cierto acceso a cosas pero que el admin tenga la opcion de modificar el stock o eliminarlo, que el cliente no pueda eliminar ni tenga privilegios de admin. ademas tienes que ver las fotos reales de los productos 
**Respuesta de la IA:** La IA estructuro la landing page publica, la logica de sesiones para roles de usuario y administrador, la gestion del carrito con descuento automatico en el JSON y las rutas para modificar stock y eliminar productos, ademas de agregar imagenes reales de los productos y validar que todo funcione.  
**Que se uso o modifico:** Se integro la navegacion completa en HTML y Django sin base de datos, separando los permisos para que solo el admin pueda editar o borrar registros del catalogo, se agregaron las rutas para que el admin pueda editar o borrar productos, ademas separamos las rutas de admin y las rutas de publico para que no se esten mezclando y se ve bien ordenado y un cliente no tenga privilegios de admin. Agrego imagene sreales de los productos ya que estaban fallando o parpadeando

## Consulta 9
**Prompt Textual:** necesito que analices todo muy bien y que hagas pruebas o que funcione todo esto. ve si las imagenes corresponden a los productos con sus precios y descripciones y ademas ve si todo el codigo esta simple y documentado para cuando yo lo lea pueda entender facilmente. ademas quiero que hagas pruebas tanto de cliente cliente como admin admin para saber si todo esta funcionando bien. no hay base de datos y no habra, usaremos solamente html  
**Respuesta de la IA:** La IA valido las 40 imagenes con sus productos y precios, agrego la marca y descripcion tecnica en detalle.html, corrigio el conflicto de rutas con el admin de Django renombrandolas a gestion/, y desarrollo 17 pruebas unitarias en tests.py verificando ambos roles al 100%.  
**Que se uso o modifico:** Se adoptaron las correcciones de diseño en las plantillas, se organizo el resumen con tarjetas estadisticas y se ejecutaron las pruebas automatizadas satisfactoriamente, la IA se dio cuenta que estaba en local y me dijo que podia usar otra forma de ejecutar las pruebas pero no queria hacer muchas cosas asi que lo dejamos en loca para poder mostrarlo en clases. ademas me advirtio de algunas vulnerabilidades de seguridad, pero fuera de todo eso hizo las modificaciones correspondientes de imagenes, validaciones de stock, precios y descripciones. 



---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## Parte 2: Explicacion del proceso

1. **¿Como usaste a la IA?** Empece pidiendole ayuda para configurar el entorno porque no recordaba los comandos, luego le pase la pauta para poder ver el enfoque o sobre que se referia esta evaluacion y me planifique y vi cosas para que la IA me pudiera ayudar a agilizar los tiempos y demorarme un poco menos. Luego lo fui guiando y corrigiendo a medida que avanzabamos para que todo funcionara correctamente para que todo funcionara bien y poder entender que hacia. ahi lo importante de pedirle que me documentara todo lo hacia y para que servia cada cosa y asi poder entenderlo mejor. Luego le pedi que me agregara las imagenes ya que las intente agregar yo pero fue muy demoroso en encontrar imagenes que sirvieran asi que le di permisos para que pudiera buscarla en sodimac o falabella y asi ahorrarme el tiempo de eso. Tambien le pedi que me creara el login con las credenciales de user y admin asi funciona todo y se puede ver de ambas perspectivas y el user tiene algunas limitaciones y el admin puede modificar o quitar el stock, ademas de poder agregar productos y borrar productos.
2. **¿Que le pediste y por que?** Le pedi que me generara los datos del JSON porque inventar 40 productos a mano tomaba mucho tiempo y ademas las ecuaciones matematicas correspondientes para que me ayudara con la logica de mostrar por ejemplo los productos agotados o las cosas requeridas en la pauta  ya que como se haria sin base de datos hacia que todo fuera mas complicado de entender pero almacenando todo en html se simplifico un poco todo. le pedi ademas que me ayudara tanto en los logins, buscar las imagenes, descripcion y precios de los productos ya que era muy demoroso encontrar imagenes que sirvieran y quedaran bien con el producto y sus ecuaciones respectivas ya que son complejas. Le pedi que hiciera algunas pruebas o testing para saber que todo funcionara y asi quedo todo completo. 
3. **¿Que respuestas te sirvieron tal cual y cuales tuviste que corregir?** La mayoria de las respuestas me sirvieron, pero tuve que corregir algunas cosas como por ejemplo el codigo de algunas vistas ya que no entendia del todo el contexto o a veces las respuestas eran muy largas y no iban al punto, asi que preferi editarlas y poder entenderlas como tal y las funciones que tendrian y para que. Le pedi que me explicara con detención algunas cosas ya que habia cosas que no entendia y cuando me hizo el tema de ls imagenes me habia dado salieron malas y tuve que buscar otra solucion y de hecho tuve que cambiar el nombre de algunas rutas para que no chocaran con las de admin y funcionara correctamente y no generara ningun error o etc. Tambien las ecuaciones que me daba no eran validas o no las entendia, asi que le pedi que me generara otro tipo de ecuaciones que fueran mas simples y faciles de entender y de modificar. Tambien las respuestas que me daba la IA eran demasiadas extensas por lo que le pedi que me diera los daos mas importantes, resumidos y claros para poder entenderlo mejory no ver tanto texto.  
4. **¿Que aprendiste en el proceso?** Aprendi a como poder usar o implementar la IA en procesos de programacion, como por ejemplo, agilizar tiempos, dejar las cosas mas claras y poder tener una guia de lo que hay que hacer para ir avanzando de manera correcta y sin perder el foco. Ademas le pedi que me generara todo el codigo comentado con documentacion para asi poder entender para que funciona cada cosa, como se conectan y todo eso para luego poder entenderlo mejor y poder modificcarlo a mi gusto. aprendi que los task y planes de planificaicon que hay que tener antes de poder generar todo son imortantes para saber o donde poder guiarte e ir completando la cosas paso a paso. Tambien aprendi que es importante no depender tanto de la IA y entender de que se trata el proceso para poder manejarlo a mi gusto y que quede como yo quiero ya que muchas veces te genera cosas que no son necesarias o no son importantes y solo te atrasan. 
