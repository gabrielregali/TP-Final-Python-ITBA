import sqlite3
from dateutil.parser import parse
from datetime import datetime, timedelta
import pandas as pd


def depurar_Resumen():
    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res2=cursor.execute("""
    SELECT resumen.Ticker, resumen.Fecha_Inicio, resumen.Fecha_Fin
    FROM resumen
    """)

    listado_tickers=[]

    for row in res2:
        listado_tickers.append(row[0])  #guardo ticker

    #elimino tickers repetidos
    resum_unic_tickers=[]
    for h in listado_tickers:
        if h not in resum_unic_tickers:
            resum_unic_tickers.append(h)

    ticresum=[]
    fecha_ini=[]
    fecha_fin=[]
    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res3=cursor.execute("""
    SELECT resumen.Ticker, resumen.Fecha_Inicio, resumen.Fecha_Fin
    FROM resumen
    """)

    
    ticresum_por_ticker=[]
    fechaini_por_ticker=[]
    fechafin_por_ticker=[]
    for p in resum_unic_tickers:
        res4=cursor.execute(f"""
        SELECT resumen.Ticker, resumen.Fecha_Inicio, resumen.Fecha_Fin
        FROM resumen
        WHERE resumen.Ticker='{p}';
        """)

        for row in res4:
            fit = parse(row[1])
            fi = datetime.date(fit) 
            fientt=int(fi.strftime("%Y%m%d"))

            fft = parse(row[2])
            ff = datetime.date(fft)
            ffentt=int(ff.strftime("%Y%m%d"))

            ticresum.append(row[0])
            fecha_ini.append(fientt)    #guardo fecha de inicio 
            fecha_fin.append(ffentt)    #guardo fecha de fin

        ticresum_por_ticker.append(ticresum)
        fechaini_por_ticker.append(fecha_ini)
        fechafin_por_ticker.append(fecha_fin)
        
        fecha_ini=[]
        fecha_fin=[]
        ticresum=[]

    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()

    res5=cursor.execute("""
    SELECT resumen.Ticker, resumen.Fecha_Inicio, resumen.Fecha_Fin
    FROM resumen
    """)
    fidb=[]
    ffdb=[]
    tic=[]

    for p in resum_unic_tickers:
        for row in res5:
            tic.append(row[0])
            fidb.append(row[1])
            ffdb.append(row[2])

    for f in range((len(fidb))):
        for e in range(len(fechaini_por_ticker)):
            fit = parse(fidb[f])
            fi = datetime.date(fit) 
            fient=int(fi.strftime("%Y%m%d"))

            fft = parse(ffdb[f])
            ff = datetime.date(fft)
            ffent=int(ff.strftime("%Y%m%d"))
                
            for fe in range(len(fechaini_por_ticker[e])):
                if ticresum_por_ticker[e][fe]==tic[f] and fient>fechaini_por_ticker[e][fe] and fient<fechafin_por_ticker[e][fe] and ffent>fechaini_por_ticker[e][fe] and ffent<fechafin_por_ticker[e][fe]:
                    fientsrt=str(fient)
                    ffentstr=str(ffent)

                    fii = datetime.strptime(fientsrt, '%Y%m%d')
                    fii2 = datetime.date(fii)

                    fff = datetime.strptime(ffentstr, '%Y%m%d')
                    fff2 = datetime.date(fff)

                    data=(tic[f], fii2, fff2)
                    cursor.execute("INSERT INTO final (Ticker, Fecha_inicio, Fecha_Fin) VALUES(?, ?, ?)", data)
                    con.commit()



    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res2=cursor.execute("""
    SELECT final.Ticker, final.Fecha_Inicio, final.Fecha_Fin
    FROM final
    """)


    Ticker_def=[]
    Fechaini_def=[]
    Fechafin_def=[]
    for row in res2:                  #guardo en lista datos a eliminar desde tabla "final"
        Ticker_def.append(row[0])   
        Fechaini_def.append(row[1])   
        Fechafin_def.append(row[2])
  

    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res3=cursor.execute("""
    SELECT resumen.Ticker, resumen.Fecha_Inicio, resumen.Fecha_Fin
    FROM resumen
    """)     
    for row in res3:                   #guardo en lista datos de la tabla "resumen"
        Ticker_def.append(row[0])   
        Fechaini_def.append(row[1])   
        Fechafin_def.append(row[2])   

    datos3={
        "Ticker": Ticker_def,
        "Fecha_Inicio": Fechaini_def,
        "Fecha_Fin": Fechafin_def
        }


    con = sqlite3.connect('TICKERS.db')
    cursor = con.cursor()
    res2=cursor.execute("""
    DELETE FROM final;
    """)
    con.commit()


    Tickers_Total_total=pd.DataFrame(data=datos3)
    Tickers_Total_total=Tickers_Total_total.drop_duplicates(keep=False)

    Tickers_Total_total = Tickers_Total_total.sort_values(['Ticker', 'Fecha_Inicio'],ascending=True)
    return Tickers_Total_total