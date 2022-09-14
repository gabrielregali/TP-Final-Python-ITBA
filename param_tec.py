import pandas as pd
import matplotlib.pyplot as plt


def param_tec(datos, grafico_ticker):
    Total_Tickers=pd.DataFrame(data=datos)
    Total_Tickers=Total_Tickers.set_index("Ticker")
    Mostrar=Total_Tickers.loc[grafico_ticker,:]
    Mostrar = Mostrar.sort_values('Fecha',ascending=True)
    x=Mostrar["Fecha"]
    y1=Mostrar["Cierre"]
    
    print("\n")
    print("¿Desea visualizar parámetros técnicos del ticker seleccionado?")
    print("1. Deseo visualizarlos")
    print("2 (O cualquier otra tecla). No deseo visualizarlos")
    param= input("Su respuesta: ")
    print("\n")

    y5= Mostrar['SMA_5']=y1.rolling(5, min_periods=1).mean()
    y7=Mostrar['EMA_0.1'] = y1.ewm(alpha=0.1, adjust=False).mean()

    if param=="1":
        fig, axs = plt.subplots(2, sharex=True)
#        fig.suptitle("Ticker: "+grafico_ticker)
        plt.xticks(rotation=90)
        fig.set_figheight(12)
        fig.set_figwidth(14)
        axs[1].plot(x, y1.pct_change()*100, color="#53868B", linewidth=2, label="Variac. Porcent.")
        axs[1].set_ylabel('Variación % Precio Cierre')
        axs[1].legend(loc='upper left')
        axs[0].plot(x, y1, color="blue", linewidth=1.5, label="Cierre")
        axs[0].plot(x, y5, color="orange", linewidth=2.5, label="SMA_5")
        axs[0].plot(x, y7, color="#66CD00", linewidth=2.5, label="EMA_0.1")
        axs[0].set_ylabel('Precio (USD)')
        axs[0].legend(loc='upper right')
        plt.show()
        print("\n")
        return
    else:
        None
        return
    
