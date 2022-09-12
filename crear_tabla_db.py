import sqlite3

def crear_tabla_db():
    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res = cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickers (
    Ticker STRING,
    Fecha STRING,
    Apertura FLOAT,
    Cierre FLOAT,
    Bajo FLOAT,
    Alto FLOAT,
    Volumen INTEGER);
    """)
    con.close()

    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res = cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumen (
    Ticker STRING,
    Fecha_Inicio STRING,
    Fecha_Fin STRING);
    """)
    con.close()

    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res = cursor.execute("""
    CREATE TABLE IF NOT EXISTS final (
    Ticker STRING,
    Fecha_Inicio STRING,
    Fecha_Fin STRING);
    """)
    con.close()
    return

