# TP-Final-Python-ITBA
TP Final Certificación Profesional Python ITBA 2022

## Resumen

Se implementa un programa en código Python, que lee datos de una API de finanzas (https://polygon.io/docs/stocks/getting-started), los guarda en una base de datos y los grafica, de acuerdo a lo solicitado en la consigna (ver Consigna TP Final.md)

## Consideraciones iniciales

El código se programó y probó en primera instancia en notebooks de Google Colab (https://colab.research.google.com/). 
Luego se probó y modularizó en el IDE Spyder versión 4.2.5, perteneciente a la distribución libre Anaconda (https://www.anaconda.com/products/distribution). 
Finalmente se probó en un notebook de Jupyter.

Las imágenes que se encuentran en este informe corresponden a capturas de pantalla de Google Colab y del IDE Spyder.


## Descripción del código en Python del programa

El corazón del programa es el script denominado "main.py", el cual realiza el llamado a funciones, que serán descriptas más adelante en este informe.

Este script comienza con la declaración de la Clase Ticker, la declaración de la función "guardar_datos_db", para luego comenzar con el llamado a la función "crear_tabla_db". Luego de esto realiza el llamado a la función "imprimir_Menu_Ppal".

#### Clase "Ticker"
- El Inicializador recibe como parámetros el nombre del ticker, una lista con todos los precios de aperturas, una lista con todos los precios de cierre, una lista con todas las fechas, una lista con todos los precios bajos, una lista con todos los precios altos, una lista con todos lo volumenes, y guarda estos datos en sus respectivas variables y listas.

![image](https://user-images.githubusercontent.com/88169218/189552511-42a7756d-518c-4d9a-aaba-97ab0f0cde87.png)

- Estos datos se envían como parámetros cuando se llama al método de la clase "agregar_datos", cuando se obtienen datos del API que deben ser guardados, como se puede ver en la siguiente parte del código (se describirá con más detalle en adelante):

![image](https://user-images.githubusercontent.com/88169218/189552421-b2046162-eb65-4eb1-97ad-d73bc1302416.png)


#### Función "crear_tabla_db"
Esta función crea 3 tablas SQL: "tickers", "resumen" y "final", en el caso que no existan (se explicarán el uso de estas tablas más adelante en este informe). Esto quiere decir que cuando se ejecuta el programa por primera vez se crean las 3 tablas para un posterior uso, pero luego de ingresar por segunda vez las tablas ya existen, por lo cual el código detecta esto y no las vuelve a crear, evitando que el programa se detenga con un error.
Utiliza la librería sqlite3.

![image](https://user-images.githubusercontent.com/88169218/189502333-d96a5245-eda7-4bb6-84a2-90b0dca68d28.png)

#### Menú principal (función "imprimir_Menu_Ppal")
El Menú Principal se llama desde Main.py mediante la función "imprimir_Menu_Ppal". Este Menú permite seleccionar entre la Actualización de datos (opción 1), o la Visualización de datos (opción 2), los cuales son solicitados para ser ingresados por el usuario. Si se presiona cualquier tecla diferente a "1" o "2" finaliza el programa.

![image](https://user-images.githubusercontent.com/88169218/189491165-d9f43d7a-7bba-4be7-92e4-330b9f9f2fbe.png)

cuando se ejecuta este código, se observa lo siguiente:

![image](https://user-images.githubusercontent.com/88169218/189489313-17839b56-50a9-4f2e-8618-efb3973cce92.png)

Esta selección se implementa en el código mediante un bucle "while", el cual se sigue ejecutando mientras el usuario presione "1" o "2", y se sale del mismo al presionar cualquier otra tecla, por ejemplo "s":

![image](https://user-images.githubusercontent.com/88169218/189493035-292cb84a-7995-4e59-989f-504e2fea4026.png)


### Actualización de Datos (Opción 1)

Cuando el usuario presiona "1", se accede al interior del while, y luego mediante un if se accede a la actualización de datos para posteriormente guardarlo en una tabla de una base de datos SQL.

![image](https://user-images.githubusercontent.com/88169218/189496481-4409cc9d-5a99-4599-bea8-5fef502c12a9.png)

Una vez dentro del if, se solicita al usuario que ingrese un ticker. Debido a que el usuario puede ingresar estos caracteres en letras minúsculas, se convierten en mayusculas (ya que es el formato que acepta el API para su base de datos de tickers).

#### Función existe_ticker
Se procede entonces a llamar la función "existe_ticker(nombre_ticker)", a la cual se le envía como parámetro este ticker ingresado por el usuario.
La función "existe_ticker(nombre_ticker)", verifica si existe el ticker ingresado dentro de la base de datos de polygon.io. Para ello, envía un get al API con el ticker ingresado. La respuesta del API se convierte a formato json.
Se pregunta mediante un if, si el valor de la clave 'status' devuelta por el API es 'NOT_FOUND'. Si este es el caso, se retorna de la función con un False, lo cual significa que el ticker no existe en la base de datos. Si el valor de la clave'status' es diferente de 'NOT_FOUND' significa que el ticker existe, entonces se ingresa al else del if, se imprime el nombre de la compañía correspondiente y se retorna de la función con un True.
La función "existe_ticker(nombre_ticker)" utiliza la librería de Python "requests" para poder realizar el get al endpoint de polygon.io que permite saber si existe el ticker (https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker), y si es el caso el nombre de la compañia correspondiente.

![image](https://user-images.githubusercontent.com/88169218/189497093-30992e7c-36aa-41d7-9deb-2598d862d8c9.png)

De regreso en el script Main, se pregunta mediante un if si la variable existe. Si se retorna de la función "existe_ticker(nombre_ticker)" con un True (existe el API) se ingresa dentro del cuerpo del if. Si se retorna con un False (no existe el API), no se ingresa dentro del cuerpo del if y se vuelve a llamar al Menú principal para que el usuario nuevamente elija una opción (función "imprimir_Menu_Ppal").

A continuación se muestran capturas de pantalla de como actúa el programa, en el caso que se ingrese un ticker inexistente:

![image](https://user-images.githubusercontent.com/88169218/189498994-ae24408d-a584-4581-8d43-1e9463c2f42c.png)


Si el ticker existe, se ingresa dentro del cuerpo del if.

![image](https://user-images.githubusercontent.com/88169218/189499147-621587a7-4645-4ecf-b92c-963a4eac8976.png)

A continuación, lo primero que se hace es conectarse a la base de datos SQL creada, y filtrar los datos guardados, que se correspondan con el nombre de ticker ingresado. 
Esto se hace, para que posteriormente se pueda verificar mediante código, si dentro del rango de fechas de inicio y fin solicitados por el usuario, existe alguna fecha que ya fue solicitada por el usuario previamente y guardada en la base de datos. De esta manera, se evita solicitar datos al API una fecha solicitada previamente.
Ej: Si tengo guardados los datos de un ticker desde el 2022/01/01 al 2022/07/01 y se solicita desde el 2021/01/01 al 2022/07/01, el programa solicita datos al API únicamente desde el 2021/01/01 al 2021/12/31 (Extra del programa).

Se solicita entonces que el usuario ingrese una fecha de inicio y una fecha de fin (ver más adelante en este informe "Manejo de excepciones y errores del programa").
Las fechas ingresadas por el usuario en formato string, son convertidas a formato de fecha mediante la función "parse" de la librería "dateutil.parser". 
Se restan la fecha de fin menos la fecha de inicio para saber cuantos dias hay en el rango entre ambas fechas. 

![image](https://user-images.githubusercontent.com/88169218/189500612-57931f07-b172-4892-ae15-e7195de74e00.png)

Este número se convierte a entero y se utiliza en un bucle for, para guardar las fechas existentes dentro del rango solicitado, en una lista (lista_fechas). Se utiliza la funcion datetime (para tomar solo la fecha del formato) a las cuales se le suma un día mediante la funcion timedelta (ambas importadas desde la librería "datetime").

![image](https://user-images.githubusercontent.com/88169218/189500165-f5f108c8-59ab-4d0d-af5e-6f7be5a34930.png)

Se guardan en una lista (fechas_db) las fechas existentes en la base de datos del ticker solicitado (previamente filtradas al conectarse a la base de datos SQL).

![image](https://user-images.githubusercontent.com/88169218/189502421-8c31f34b-e8b1-475b-98e3-02b0b597a25c.png)

Entonces se comprueba mediante un bucle for si las fechas que se encuentran entre el rango solicitado por el usuario (lista_fechas), ya existen dentro de la base de datos (fechas_db). 
En el caso de que no existan dentro de la base de datos del ticker pedido, se guardan en una nueva lista (lista_fechas_fin), la cual se utilizará para solicitar datos al API de Polygon.io (de esta manera se evita solitar datos de una fecha a la cual ya se le solicitaron datos con anterioridad).

![image](https://user-images.githubusercontent.com/88169218/189502589-a7137dd6-2338-4121-89dc-7e133899b89b.png)

Entonces, se solicitan datos del ticker al API de Polygon.io, realizando un get por fecha guardada en la lista de fechas no repetidas en la base de datos (lista_fechas_fin).
Debido a que la versión gratuita de este API tiene una limitación de 5 llamadas por minuto, se realiza una llamada a la función "sleep" por 12 segundos, para evitar superar el número de llamadas por minuto.
Esta versión gratuita tiene la limitación de que no devuelve datos de fechas anteriores a 2 años a la fecha.
En el caso que se utilice una versión paga de este API, se podría eliminar la espera de 12 segundos por llamada al API, haciendo que el programa sea más veloz.

![image](https://user-images.githubusercontent.com/88169218/189502717-a22ed57f-0a1f-4a4d-9312-3865f0716da6.png)

NOTA IMPORTANTE: Se utilizó el siguiente endpoint de Polygon.io: https://polygon.io/docs/stocks/get_v3_quotes__stockticker .
Este API permite obtener datos de sólo una fecha al realizar un get.
Se seleccionó el anterior endpoint, por sobre el endpoint https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to . El último devuelve datos de varias fechas selecionadas en un rango solicitado, pero tiene la desventaja que no indica las fechas a las cuales corresponden estos datos y no devuelve datos de días feriados, sábados y domingos, por lo cual se hace imposible identificar los datos para poder trabajar con ellos posteriormente.

Los datos que devuelve el API se convierten a formato json.
Se pregunta mediante un if si no existen datos en esa fecha ('status'=='NOT_FOUND'), en cuyo caso los datos no se guardan en la clase Ticker (ver más abajo explicación de Clase Ticker)
Si existen datos (else del if) se guardan los datos del json en la clase Ticker, mediante el método "agregar_datos" de la clase.

![image](https://user-images.githubusercontent.com/88169218/189503093-af73b69b-047b-4be2-9b92-3fa1fdd7c2c6.png) 

Una vez que se guardaron los datos obtenidos en la clase Ticker, se guardan estos datos en la base de datos SQL en la tabla "tickers", mediante la función "guardar_datos_db".
Por último se llama nuevamente al Menú Principal.

![image](https://user-images.githubusercontent.com/88169218/189503305-46163b48-25e8-44b7-942c-3f034775c7fd.png)

#### Función guardar_datos_db
Esta función se conecta con la base de datos SQL y guarda mediante un bucle for, los datos que previamente se guardaron en la Clase Ticker. 

![image](https://user-images.githubusercontent.com/88169218/189504700-72828c31-1c60-4ed2-a63e-31fa497fab37.png)

![image](https://user-images.githubusercontent.com/88169218/189504723-ca8f6566-a355-4396-943d-cc8d5e768fac.png)

Se guardan en 2 tablas. 
En la tabla "tickers" se guardan el Ticker, la Fecha, el precio de Apertura, el precio de Cierre, el precio más Bajo, el precio más Alto, el Volumen operado. Estos datos se utilizarán posteriormente para graficar los datos en el Menú de Visualización.
En la tabla "resumen" se guardan el ticker, la fecha de inicio, la fecha de fin, los cuales serán utilizados posteriomente para visualizar en el Menú Resumen.

Cuando se ejecuta el código descripto anteriormente, se observa lo siguiente:

![image](https://user-images.githubusercontent.com/88169218/189531589-5649fdbc-8e6d-434f-b097-9a6aceca8778.png)

![image](https://user-images.githubusercontent.com/88169218/189531644-9c0ac010-e995-4e14-806c-0213435202c2.png)

Si vuelvo a solicitar datos, pero en un rango de fechas para la cual ya solicité datos previamente, el código sólo solicitará datos al API de las fechas nunca pedidas antes:

![image](https://user-images.githubusercontent.com/88169218/189531864-b29f7316-1fba-4639-b31d-0b6e79eb65c7.png)

como se puede observar, no se solicitaron datos al API para el 6 y 7 de julio, ya que habían sido solicitados previamente.


### Visualización de Datos (Opción 2)

Si el usuario presiona "2", mediante un elif de la opción 1, se accede a la visualización de los datos que se encuentran guardados en la base de datos SQL.
A continuación el código se conecta con la base de datos, y mediante bucles for se guardan los datos en dos diccionarios: 
- en el diccionario datos se guardan los datos de la tabla "tickers".
- en el diccionario datos2 se guardan los datos de la tabla "resumen"

![image](https://user-images.githubusercontent.com/88169218/189505213-d63f66b7-1b48-42ba-aff2-74664d6505f1.png)

![image](https://user-images.githubusercontent.com/88169218/189505202-c74f23ad-b244-4b0a-a84e-378f7530934f.png)

![image](https://user-images.githubusercontent.com/88169218/189505222-1730e56f-06e2-4e7e-b012-6bf95d7a5112.png)

Los datos guardados en estos 2 diccionarios se utilizan para armar 2 Dataframe:
- El dataframe "Total_Tickers" se utiliza para graficar posteriormente los datos de los tickers
- El dataframe "Resumen_Tickers" se utiliza para mostrar posteriormente un resumen de los datos solicitados por ticker, por rango de fechas.

![image](https://user-images.githubusercontent.com/88169218/189550532-9970076b-e034-4232-8707-02fee71cf484.png)

Finalmente se llama al Menú de Visualización mediante la función "imprimir_Menu_Visualiz".

Este Menú permite seleccionar entre visualizar un Resumen de los tickers que se solicitaron previamente con sus rangos de fechas correspondientes (opción 1), o el gráfico de Precios de Cierre, Bajo y Alto por fechas guardados en la base de datos SQL, de un ticker que posteriormente deberá ingresar el usuario (opción 2). Si se presiona cualquier tecla diferente a "1" o "2", se vuelve al Menú Principal.

![image](https://user-images.githubusercontent.com/88169218/189505416-b65da5bd-5a4f-4db0-b14f-2a9828d13861.png)

Si se presiona "1" o "2" se ingresa dentro de un bucle while del que se sale presionando cualquier tecla diferente a estas 2 opciones.

### Submenú Resumen (Opción 1)
Dentro del bucle while, si se presiona "1" se ingresa dentro del cuerpo de un if, el cual es el código encargado de mostrar el Resumen de los tickers guardados en la base de datos hasta el momento, el cual se puede ver en el dataframe "Resumen_Tickers".
Pero, en este dataframe se guardan todas la fechas solicitadas al API, por lo cual si se solicito una fecha incluida dentro de otro rango de fechas, se muestran ambas solicitudes, como se puede observar en la siguiente imagen:

![image](https://user-images.githubusercontent.com/88169218/189532662-f1a7f847-85ed-460a-9fcc-f270bac426ce.png)

en la que se puede ver que el intervalo desde el 6 al 7 de julio se encuentra dentro del intervalo del 5 al 8 de julio. 
Debido a esto se creó la funcion "depurar_Resumen" la cual verifica rangos de fechas incluidos dentro de otros rangos de fechas y los unifica, es decir hace que se muestre un rango de fechas del 5 al 8 de julio (ya que desde el 6 al 7 se encuentra incluido en el rango anterior).

NOTA IMPORTANTE: Unificar 2 rangos de fechas, prevaleciendo el rango más amplio, seguramente se puede realizar sencillamente mediante código SQL, en algo que encontré en la web que se denomina islas y huecos (o islands and gaps): https://www.mssqltips.com/sqlservertutorial/9130/sql-server-window-functions-gaps-and-islands-problem/ .
Probé código SQL para agrupar los rangos de fechas, pero no obtuve buenos resultados, por lo cual realicé esta agrupación mediante Python. 
El código se encuentra dentro de la función "depurar_Resumen", la cual realiza esta agrupación exitosamente, pero probablemente se pueda optimizar en menos líneas de código.

#### Función depurar_Resumen
Esta funcion se conecta con la tabla "tickers" de la base de datos, y mediante bucles for guarda en una lista los nombres de tickers no repetidos (resum_unic_tickers):

![image](https://user-images.githubusercontent.com/88169218/189533536-23582cb6-1d73-4933-907c-ed26330ecd9d.png)

Luego, se conecta nuevamente a la tabla "resumen" de la base de datos, filtra los datos por nombre de ticker, y mediante 2 bucles for guarda en 2 listas de listas las fechas de inicio y fin para cada ticker:

![image](https://user-images.githubusercontent.com/88169218/189535124-c076e913-e5f3-4106-a64d-0bff27b7104a.png)

Entonces, se conecta nuevamente con la tabla "resumen" de la base de datos, y se guardan todas las fechas existentes y nombres de tickers en 3 listas mediante un bucle for:

![image](https://user-images.githubusercontent.com/88169218/189535265-c3c32f44-974a-4431-999e-6b9cf35746fb.png)

Finalmente, se comparan mediante 2 bucles for anidados, las fechas totales de inicio y fin guardadas en 2 listas de la totalidad de la tabla resumen, contra las fechas de inicio y fin guardadas por ticker en las 2 listas de listas.

Si se encuentra que un par de fecha de inicio-fecha de fin se encuentra incluida dentro de otro par de fecha de inicio-fecha de fin (correspondientes a un mismo ticker), significa que se trata de fechas incluidas en otro rango de fechas, entonces se guardan estas fechas en una tabla llamada "final" de la base de datos: 

![image](https://user-images.githubusercontent.com/88169218/189535328-7d1a3391-d266-4acc-9634-1caf7953ae92.png)

El código se conecta entonces con las tablas "resumen" y "final" de la base de datos, y guarda en 3 listas todos los datos incluidos en estas 2 tablas. Estas listas se utilizan para guardar los datos en un diccionario, el cual se utiliza para crear el dataframe "Tickers_Total_total":

![image](https://user-images.githubusercontent.com/88169218/189536015-0a996c0f-1cc6-44c0-af16-ee38ed62641d.png)

![image](https://user-images.githubusercontent.com/88169218/189536038-b3976de5-2d34-493d-9be4-e2e2a3e69fb1.png)

Finalmente, en el dataframe "Tickers_Total_total" se eliminan los datos duplicados, es decir los que separaron en la tabla "final" de la base de datos por encontrarse incluidos en otro rango de fechas.
De esta manera, el dataframe "Tickers_Total_total" posee solo los rangos de fecha mas abarcativos por ticker, ordenados de manera ascendente por nombre de ticker y fecha:

![image](https://user-images.githubusercontent.com/88169218/189536048-0e9ea276-d7e8-4c7a-9eb6-0a114ab8adc0.png)

Utilizando ahora la función "depurar_Resumen"  se pude observar en las siguientes imágenes como se soluciona lo comentado anteriormente:

SIN  "depurar_Resumen"

![image](https://user-images.githubusercontent.com/88169218/189532662-f1a7f847-85ed-460a-9fcc-f270bac426ce.png)

CON  "depurar_Resumen"

![image](https://user-images.githubusercontent.com/88169218/189536605-1e58d476-9d85-462a-9fe3-3a249584457c.png)


### Submenú Gráfico de Ticker (Opción 2)
Dentro del bucle while, si se presiona "2" se ingresa dentro del cuerpo del elif, el cual es el código encargado de graficar los datos del ticker que desee el usuario.

Se utiliza para graficar el dataframe "Total_Tickers", el cual posee los datos actualizados de la tabla "tickers" de la base de datos SQL.
Se solicita en primer lugar que el usuario ingrese un ticker. A continuación existen 3 posibilidades:
- Que al solicitar el ticker la tabla esté vacía ya que todavía no se han guardado datos
- Que el ticker no esté guardado aún en la base de datos por lo cual no se puede graficar
- Que se solicite un ticker que posee datos guardados y se pueda graficar.

- Si al solicitar el ticker la tabla está vacía (ya que todavía no se han guardado datos), se imprime un mensaje indicando esto.

![image](https://user-images.githubusercontent.com/88169218/189547018-44fd9965-75f6-4d11-b3c8-e851e649c7ea.png)

- Si el ticker no está guardado aún en la base de datos no se puede graficar, por lo cual se sale por el else del if indicando esto. Se llama nuevamente al Menú de Visualización para que el usuario escoja una opción.

![image](https://user-images.githubusercontent.com/88169218/189547077-62a43735-481f-484a-ae50-b3f3ffb5ab9b.png)

- Si se solicita un ticker que posee datos guardados y se pueda graficar, se filtra el dataframe por el nombre del ticker que desee el usuario, mostrando solo los datos correspondientes a este ticker.

![image](https://user-images.githubusercontent.com/88169218/189547172-cbf2db5d-382b-4f34-817b-02f6b816ca1f.png)

En un mismo gráfico se muestran los datos guardados del ticker en la base de datos: nombre del ticker, precio más bajo, precio más alto y precio de cierre por fecha. El precio de cierre se grafica en una linea más gruesa. 

Cuando se ejecuta el código descripto anteriormente, se observa lo siguiente:
- Si se ingresa un ticker que no existe en la base de datos:

![image](https://user-images.githubusercontent.com/88169218/189549660-e9596c2a-075c-4b85-b7a3-ec1ac5df6686.png)

- Cuando se ingresa un ticker existente en la base de datos:

![image](https://user-images.githubusercontent.com/88169218/189549697-bc03f841-7d2b-43fb-824e-46d65f0eb8a3.png)

![image](https://user-images.githubusercontent.com/88169218/189549725-c3cff04d-a8e9-446d-954b-5b00d0a7df1e.png)

#### Función param_tec (Extra)
Esta función se encarga de graficar parámetros técnicos, en el caso que lo desee el usuario. 
Estos parámetros son la Variación Porcentual del Precio de Cierre de una Fecha a la siguiente que este guardada en la base de datos, 
la media móvil simple (SMA por sus iniciales en inglés), y la media móvil exponencial (EMA por sus iniciales en inglés).

Luego de graficar el ticker solicitado por el usuario, se pregunta si desea visualizar parámetros técnicos de este mismo ticker. 
En el caso que presione "1" se entra en el cuerpo del if el cual se encarga de graficar los parámetros mencionados. Si se presiona otra tecla diferente a "1" se vuelve al Menú de Visualización.

![image](https://user-images.githubusercontent.com/88169218/190029335-2d1627e6-bbaf-4361-ab87-98d358dbd9c1.png)

![image](https://user-images.githubusercontent.com/88169218/190029394-948978fa-2f47-4de8-99c6-b20551889789.png)

- Media móvil simple (SMA), y Media móvil exponencial (EMA).
La media móvil simple (SMA) se calculó utilizando el método .rolling de Pandas, empleando una ventana de 5 días y un número mínimo de períodos de 1.
La media móvil exponencial (EMA) se calculó utilizando el método .ewm , empleando un factor de suavizado (alpha) de 0.1.
Ambos parámetros se graficaron en el subplot 1 de 2, junto al Precio de Cierre (este valor posee un ancho de linea menor).
https://towardsdatascience.com/moving-averages-in-python-16170e20f6c

- Variación Porcentual del Precio de Cierre
Se calcula utilizando el método .pct_change() de Pandas, el cual calcula la variación porcentual del Precio de Cierre de un día al siguiente inmediato.
Este parámetro se gráfica en el subplot 2 de 2.
https://programmerclick.com/article/81251862314/

Cuando se ejecuta el código descripto anteriormente, se observa lo siguiente en el programa:

![image](https://user-images.githubusercontent.com/88169218/190031003-3e684ed9-0ee9-493f-a33e-92135617bb03.png)

![image](https://user-images.githubusercontent.com/88169218/190031027-7da40c64-0ece-4702-9614-d3d580c9d455.png)



### Manejo de excepciones y errores del programa (Extra)
- En la función "crear_tabla_db" el código detecta si la base de datos ya tiene creadas las tablas, evitando arrojar un error y detener la ejecución del programa (explicado anteriormente).
- En la función "existe_ticker" se comprueba si existe el ticker en la API de Polygon.io, evitando que el programa se interrumpa por error cuando el usuario solicite un ticker inexistente (explicado anteriormente).
- Cuando el usuario ingresa caracteres alfanuméricos como fechas de inicio o de fin, diferentes del formato de fecha que requiere la API (YYYY-MM-DD), mediante un códido se detecta esto, se indica al usuario mediante un mensaje que una de las fechas tiene un formato incorrecto y se le vuelve a solicitar que ingrese las fechas.
- Este código se obtuvo de la documentación que ofrece la página web de Python (8.3. Handling Exceptions): https://docs.python.org/3/tutorial/errors.html

![image](https://user-images.githubusercontent.com/88169218/189551187-5f377248-61eb-40e6-a311-4513e739d881.png)

- Cuando el usuario ingresa una fecha, con un formato erróneo menor a 10 caracteres correspondientes a AAAA-MM-DD, se detecta esto mediante código, se indica al usuario mediante un mensaje que una de las fechas tiene un formato incorrecto y se le vuelve a solicitar que ingrese las fechas

![image](https://user-images.githubusercontent.com/88169218/189551297-217cb5d0-2a6b-4cf0-89c7-f97a3ec4dc8e.png)

- Si el usuario ingresa una fecha de inicio mayor que la fecha de fin, el código detecta esto, evitando errores en la solicitud de datos al API o cuando se guardan datos en la base de datos.
Se le indica este error al usuario y se le solicita que ingrese las fechas nuevamente.

![image](https://user-images.githubusercontent.com/88169218/189551357-726df78f-3d6c-44f7-9c4f-8c37f849d1ea.png)

Cuando se ejecuta el código descripto anteriormente, correspondiente a errores del usuario al ingresar las fechas se observa lo siguiente:

Cuando el usuario ingresa caracteres alfanuméricos en vez de fechas:

![image](https://user-images.githubusercontent.com/88169218/189551459-18c88bf7-bc13-4392-8095-6339d7f49cfe.png)

Cuando el usuario ingresa fechas con menos de 10 caracteres (formato AAAA-MM-DD):

![image](https://user-images.githubusercontent.com/88169218/189551492-4a81fc68-7a89-47e2-a9d6-afa921c01fa2.png)

Cuando el usuario ingresa una fecha de inicio mayor a la fecha de fin:

![image](https://user-images.githubusercontent.com/88169218/189551541-0c060aa5-7abd-4422-b8c0-b33352e831f3.png)




## Desarrolladores del Proyecto
El código de este programa, y el informe de funcionalidad y diseño, fue realizado en su totalidad por Gabriel Alfredo Regali (https://github.com/gabrielregali) .

## Repositorio de Github
En el repositorio de github se encuentran los siguientes archivos (https://github.com/gabrielregali/TP-Final-Python-ITBA):

- README.md:  Informe de funcionalidad y diseño.
- Consigna TP Final.md: Consigna TP Final Certificación Profesional Python.

- main.py: Script que contiene el programa principal del proyecto.
- crear_tabla_db.py: Script que contiene la función encargada de la creación de tablas en la base de datos.
- depurar_resumen.py: Script que contiene la función encargada de la depuración y optimización de los datos para Menú Resumen.
- existe_ticker.py: Script que contiene la función encargada de verificar si existe el ticker solicitado en API de Polygon.io
- imprimir_Menu_Ppal.py: Script que contiene la función encargada de imprimir el Menú Principal y solicitar una elección al usuario.
- imprimir_Menu_Visualiz.py: Script que contiene la función encargada de imprimir el Menú de Visualización y solicitar una elección al usuario.
- param_tec.py: Script que contiene la función encargada de calcular y graficar parámetros técnicos (SMA, EMA, Variación Porcentual, todos calculado sobre el Precio de Cierre).

- Base de datos SQL llamada "TICKERS" (posee las tablas "tickers", "resumen" y "final"), en la cual se puede verificar que se grabaron los datos mediante el código de Python y que se puede utilizar para probar las visualizaciones, con datos ya solicitados al API durante las pruebas realizadas al programar el código del proyecto.

- Notebook de Google Colab (.ipynb) con el programa completo del proyecto.
