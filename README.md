# TP-Final-Python-ITBA
TP Final Certificación Profesional Python ITBA 2022

## Resumen

Se implementea un programa en código Python, que lee datos de una API de finanzas (https://polygon.io/docs/stocks/getting-started), los guarda en una base de datos y los grafica, de acuerdo a lo solicitado en la consigna (ver Consigna Final Tp.md)



## Informe de funcionalidad y diseño

### Menú principal

El programa debe presentar un menú principal donde puedan elegirse las siguientes dos opciones:

 1. Actualización de datos
 2. Visualización de datos

![image](https://user-images.githubusercontent.com/88169218/189489313-17839b56-50a9-4f2e-8618-efb3973cce92.png)





### Actualización de datos

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
