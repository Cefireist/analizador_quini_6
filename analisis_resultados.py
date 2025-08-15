"""
En este codigo se analizan los numeros que mas salieron en el ultimo año (2025)
en el sorteo de quini6
"""
#%%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import duckdb as db
#%%

# busco la ruta del archivo con los datos
nombre_archivo = "resultados_quini6.csv"
carpeta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(carpeta_script, nombre_archivo)

datos = pd.read_csv(ruta_csv, delimiter=",")
print(datos.head())

#%%
con = db.connect()

# Registramos el DataFrame como una "tabla" temporal
con.register("quini6", datos)

resultados_tradicional_2025 = con.execute("""
SELECT fecha, n1, n2, n3, n4, n5, n6
FROM quini6
WHERE Modalidad='Tradicional' AND fecha LIKE '2025%'
ORDER BY fecha DESC
""").df()

num_sorteos = len(resultados_tradicional_2025)
#%%

numeros = resultados_tradicional_2025[['n1','n2','n3','n4','n5','n6']].values.flatten()
valores, cuentas = np.unique(numeros, return_counts=True)

plt.figure(figsize=(16,7))

# barras más finas para que haya más separación
plt.bar(valores, cuentas, color='skyblue', edgecolor='black', width=0.6, label = f"Sorteos considerados: {num_sorteos}")  # <- width más pequeño

# etiquetas eje X
plt.xticks(range(0,46), fontsize=14, rotation=0)  # números del 1 al 45
plt.yticks(fontsize=14)

# etiquetas y título
plt.xlabel('Número', fontsize=16)
plt.ylabel('Cantidad de veces sorteado', fontsize=16)
plt.title('Distribución de números Tradicional Quini6 2025', fontsize=16)
# grilla horizontal
plt.grid(axis='y', linestyle='--', alpha=0.8, color='black')
plt.legend(fontsize = 16)
plt.tight_layout()
plt.show()


#%%
valores = np.array(valores)
cuentas = np.array(cuentas)

# ordeno de mayor a menor frecuencia
orden = np.argsort(cuentas)[::-1]
valores_ord = valores[orden]
cuentas_ord = cuentas[orden]


x_pos = np.arange(len(valores_ord))


plt.figure(figsize=(16,7))
plt.bar(x_pos, cuentas_ord, color='skyblue', edgecolor='black', width=0.6, label = f"Sorteos considerados: {num_sorteos}")

# en el eje x pongo el numero que corresponde
plt.xticks(x_pos, valores_ord, fontsize=14, rotation=0)
plt.yticks(fontsize=14)
plt.xlabel('Número', fontsize=14)
plt.ylabel('Cantidad de veces sorteado', fontsize=14)
plt.title('Distribución de números Tradicional Quini6 2025 (de mayor a menor)', fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.8, color='black')
plt.legend(fontsize = 16)

# Agregar los valores encima de cada barra
for i, cuenta in enumerate(cuentas_ord):
    plt.text(x_pos[i], cuenta + 0.1, str(cuenta), ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()



#%%