"""
Con este codigo se hace scrapping de una pagina web:
    "https://resultados-de-loteria.com/quini-6/resultados/2025"
con el fin de conseguir armar un csv con los datos del quini 6 historicos.
"""

#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
#%%
def buscar_fecha(tr):
    """
    Recibe un <tr> y devuelve la fecha del sorteo asociada
    """
    a_tag = tr.find("a")
    href = a_tag['href']
    fecha_str = href.split("/")[-1]  # "03-08-2025"
    return fecha_str

def extraer_modalidad_y_resultados(ul):
    """
    Recibe un <ul class="balls"> y devuelve la modalidad y los numeros sorteados
    """
    li_items = ul.find_all("li")

    numeros = []
    for i in range(0, len(li_items)):
      if i == 0:
        modalidad = li_items[i].text.strip()
      else:
        numeros.append(int(li_items[i].text.strip()))
    return modalidad, numeros

def scrappear_anio(resultados, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    trs = soup.find_all("tr")
    for tr in trs:
      # Extraigo la fecha
      tds = tr.find_all("td")
      if len(tds) < 2:
          continue
    
      fecha_str = buscar_fecha(tds[0])
      resultados["fecha_str"].append(fecha_str)
    
      # Extraigo las 4 modalidades y lo sorteado para esa fecha
      uls = tds[1].find_all("ul")
      uls_class_balls = [ul
                         for ul in uls
                         if ul.get("class") == ["balls"]]
    
      for ul in uls_class_balls:
        modalidad, numeros = extraer_modalidad_y_resultados(ul)
        if modalidad in resultados:
            resultados[modalidad].append(numeros)
    return resultados

#%%
resultados = {
    "fecha_str": [],
    "Tradicional": [],
    "La Segunda": [],
    "Revancha": [],
    "Siempre Sale": []
}
url_base = "https://resultados-de-loteria.com/quini-6/resultados/20"
for anio in range(25,9,-1):
    url = url_base + str(anio)
    resultados = scrappear_anio(resultados, url)
            
#%%
"""
Guardo toda la informacion en un CSV del siguiente formato:

| fecha | Modalidad | n1 | n2 | n3 | n4 | n5 | n6 |

"""
# guardo el csv como hermano de este script
nombre_archivo = "resultados_quini6.csv"
carpeta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(carpeta_script, nombre_archivo)


modalidades = ["Tradicional", "La Segunda", "Revancha", "Siempre Sale"]
datos = []

# en cada fecha hay 4 modalidades
for i, fecha in enumerate(resultados["fecha_str"]):
    for modalidad in modalidades:
        
        numeros = resultados[modalidad][i]
        
        # cada fila es un diccionario con los datos
        row = {"fecha": fecha, "Modalidad": modalidad}
        
        for j in range(0, 6):
            row[f"n{j+1}"] = numeros[j]
        
        datos.append(row)



df = pd.DataFrame(datos)
df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
df.to_csv(ruta_csv, index=False)


#%%




