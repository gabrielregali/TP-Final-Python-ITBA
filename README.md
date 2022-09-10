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


#### Menú principal (función "imprimir_Menu_Ppal")
El Menú Principal se llama desde Main.py mediante la función "imprimir_Menu_Ppal". Este Menú permite seleccionar entre la Actualización de datos (opción 1), o la Visualización de datos (opción 2), los cuales son solicitados para ser ingresados por el usuario. Si se presiona cualquier tecla diferente a "1" o "2" finaliza el programa.

![image](https://user-images.githubusercontent.com/88169218/189491165-d9f43d7a-7bba-4be7-92e4-330b9f9f2fbe.png)

cuando se ejecuta este código, se observa lo siguiente:

![image](https://user-images.githubusercontent.com/88169218/189489313-17839b56-50a9-4f2e-8618-efb3973cce92.png)

Esta selección se implementa en el código mediante un bucle "while", el cual se sigue ejecutando mientras el usuario presione "1" o "2", y se sale del mismo al presionar cualquier otra tecla, por ejemplo "s":

![image](https://user-images.githubusercontent.com/88169218/189493035-292cb84a-7995-4e59-989f-504e2fea4026.png)


### Actualización de Datos 

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
