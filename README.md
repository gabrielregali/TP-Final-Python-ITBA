# TP-Final-Python-ITBA
TP Final Certificación Profesional Python ITBA 2022

## Resumen

Se implementa un programa en código Python, que lee datos de una API de finanzas (https://polygon.io/docs/stocks/getting-started), los guarda en una base de datos y los grafica, de acuerdo a lo solicitado en la consigna (ver Consigna TP Final.md)

## Consideraciones iniciales

El código se programó y probó en primera instancia en notebooks de Google Colab (https://colab.research.google.com/). Luego se probó y modularizó en el IDE Spyder versión 4.2.5, perteneciente a la distribución libre Anaconda (https://www.anaconda.com/products/distribution).
Las imágenes que se encuentran en este informe corresponden a capturas de pantalla de Google Colab y del IDE Spyder.


## Descripción del código en Python del programa

El corazón del programa es el script denominado "Main.py", el cual realiza el llamado a funciones, que serán descriptas más adelante en este informe.
Este script comienza con el llamado a la función "crear_tabla_db". Luego de esto realiza el llamado a la función "imprimir_Menu_Ppal".

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
Ej: Si tengo guardados los datos de un ticker desde el 2022/01/01 al 2022/07/01 y se solicita desde el 2021/01/01 al 2022/07/01, el programa solicita datos al API únicamente desde el 2021/01/01 al 2021/12/31.

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

Una vez que se guardaron los datos obtenidos en la clase Ticker, se guardan estos datos en la base de datos SQL, tabla "tickers" mediante la función "guardar_datos_db".
Por último se llama nuevamente al Menú Principal.

![image](https://user-images.githubusercontent.com/88169218/189503305-46163b48-25e8-44b7-942c-3f034775c7fd.png)

#### Función guardar_datos_db
Esta función se conecta con la base de datos SQL y guarda mediante un bucle for, los datos que previamente se guardaron en la Clase Ticker. 

![image](https://user-images.githubusercontent.com/88169218/189504700-72828c31-1c60-4ed2-a63e-31fa497fab37.png)

![image](https://user-images.githubusercontent.com/88169218/189504723-ca8f6566-a355-4396-943d-cc8d5e768fac.png)

Se guardan en 2 tablas. 
En la tabla "tickers" se guardan el Ticker, la Fecha, el precio de Apertura, el precio de Cierre, el precio más Bajo, el pecio más Alto, el Volumen operado. Estos datos se utilizarán posteriormente para graficar los datos en el Menú de Visualización.
En la tabla "resumen" se guardan el ticker, la fecha de inicio, la fecha de fin, los cuales serán utilizados posteriomente para visualizar en el Menú Resumen.


### Visualización de Datos (Opción 2)

Si el usuario presiona "2", mediante un elif de la opción 1, se accede a la visualización de los datos que se encuentran guardados en la base de datos SQL.
A continuación el código se conecta con la base de datos, y mediante bucles for se guardan los datos en dos diccionarios: 
- en el diccionario datos se guardan los datos de la tabla "tickers".
- en el diccionario datos2 se guardan los datos de la tabla "resumen"

![image](https://user-images.githubusercontent.com/88169218/189505213-d63f66b7-1b48-42ba-aff2-74664d6505f1.png)

![image](https://user-images.githubusercontent.com/88169218/189505202-c74f23ad-b244-4b0a-a84e-378f7530934f.png)

![image](https://user-images.githubusercontent.com/88169218/189505222-1730e56f-06e2-4e7e-b012-6bf95d7a5112.png)

Finalmente los datos guardados en estos 2 diccionarios se utilizan para armar 2 Dataframe:
- El dataframe "Total_Tickers" se utiliza para graficar posteriormente los datos de los tickers
- El dataframe "Resumen_Tickers" se utiliza para mostrar posteriormente un resumen de los datos solicitados por ticker, por rango de fechas.

![image](https://user-images.githubusercontent.com/88169218/189505243-85303d3b-ceee-4159-af1e-e5ef87cd1416.png)

Finalmente se llama al Menú de Visualización mediante la función imprimir_Menu_Visualiz.





























### Manejo de excepciones y errores del programa


El programa debe solicitar al usuario el valor de un ticker, una fecha de inicio y una fecha de fin. Debe luego pedir los valores a la API y guardar estos datos en una base de datos SQL.

Ejemplo:
```
>>> Ingrese ticker a pedir:
AAPL
>>> Ingrese fecha de inicio:
2022/01/01
>>> Ingrese fecha de fin:
2022/07/01
>>> Pidiendo datos ...
>>> Datos guardados correctamente
```

### Visualización de datos

El programa debe permitir dos visualizaciones de datos:

 1. Resumen
 2. Gráfico de ticker

### Resumen

Debe imprimir un resumen de los datos guardados en la base de datos.

Ejemplos:
```
>>> Los tickers guardados en la base de datos son:
>>> AAPL - 2022/01/01 <-> 2022/07/01
>>> AAL  - 2021/01/01 <-> 2022/07/01
```

### Gráfico

El programa debe permitir graficar los datos guardados para un ticker específico.

Ejemplo:
```
>>> Ingrese el ticker a graficar:
AAL
```

## Condición de aprobación
El programa debe cumplir con toda la funcionalidad dentro de detalles de implementación. Para obtener una nota superior a 7 deben implementarse alguna funcionalidad extra, sea las propuestas o propuestas por el grupo.

## Extras

Posibles extras para el programa:

 - Visualización en tiempo real del valor de una acción.
 - Actualización de rangos en base de datos considerando lo guardado. Ej: Si tengo del 2022/01/01 al 2022/07/01 y pido del 2021/01/01 al 2022/07/01 únicamente debo pedir del 2021/01/01 al 2021/12/31.
 - Manejo de errores de red y reconexiones.
 - Visualización de parámetros técnicos.

## Links útiles

 1. [API de valores de finanzas] (https://polygon.io/docs/stocks/getting-started).
 2. [Libreria de base de datos] (https://docs.python.org/3/library/sqlite3.html).
