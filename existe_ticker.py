import requests

def existe_ticker(nombre_ticker):
        json_file=requests.get("https://api.polygon.io/v3/reference/tickers/"+nombre_ticker+"?apiKey=koTdrPqepxbon7yPbhPEejDv23UHe2Kw")
        json_obj = json_file.json()

        if(json_obj['status']=='NOT_FOUND'):      #si el ticker ingresado no existe
            print('El ticker ingresado no existe dentro del API de "Polygon.io"\n')
            return False
                
        else:                                     #si el ticker ingresado existe
            print("El ticker ingresado corresponde a la empresa: ", json_obj['results']['name']+"\n")
            return True
