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
from scipy.stats import chisquare
#%%

# busco la ruta del archivo con los datos
nombre_archivo = "resultados_quini6.csv"
carpeta_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(carpeta_script, nombre_archivo)

datos = pd.read_csv(ruta_csv, delimiter=",")
print(datos.head())

#%%
# Extraigo los datos del 2025 para las 4 modalidades

con = db.connect()
con.register("quini6", datos)

resultados_2025 = con.execute("""
SELECT fecha, n1, n2, n3, n4, n5, n6
FROM quini6
WHERE fecha LIKE '2025%'
ORDER BY fecha DESC
""").df()

resultados_tradicional_2025 = con.execute("""
SELECT fecha, n1, n2, n3, n4, n5, n6
FROM quini6
WHERE Modalidad='Tradicional' AND fecha LIKE '2025%'
ORDER BY fecha DESC
""").df()

resultados_la_segunda_2025 = con.execute("""
SELECT fecha, n1, n2, n3, n4, n5, n6
FROM quini6
WHERE Modalidad='La Segunda' AND fecha LIKE '2025%'
ORDER BY fecha DESC
""").df()

resultados_revancha_2025 = con.execute("""
SELECT fecha, n1, n2, n3, n4, n5, n6
FROM quini6
WHERE Modalidad='Revancha' AND fecha LIKE '2025%'
ORDER BY fecha DESC
""").df()

resultados_siempre_sale_2025 = con.execute("""
SELECT fecha, n1, n2, n3, n4, n5, n6
FROM quini6
WHERE Modalidad='Siempre Sale' AND fecha LIKE '2025%'
ORDER BY fecha DESC
""").df()

#%%
def plotear_frecuencias(resultados, modalidad):
    """
    Recibe resultados del Quini 6 y grafica con barras cuantas veces salio cada numero.
    Primer subplot: ordenado por numeros ascendente
    Segundo subplot: ordenado por frecuencias descendente
    """
    numeros = resultados[['n1','n2','n3','n4','n5','n6']].values.flatten()
    valores, cuentas = np.unique(numeros, return_counts=True)
    
    num_sorteos = len(resultados)
    
    fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(16,14), layout="constrained")
    
    # primer subplot
    axs[0].bar(valores, cuentas, color='skyblue', edgecolor='black',
               width=0.6, label=f"Sorteos considerados: {num_sorteos}")
    
    axs[0].set_xticks(range(0,46))
    axs[0].tick_params(axis='x', labelsize=14, rotation=0)
    axs[0].tick_params(axis='y', labelsize=14)
    
    axs[0].set_xlabel('Número', fontsize=16)
    axs[0].set_ylabel('Cantidad de veces sorteado', fontsize=16)
    axs[0].set_title(f'Distribución modalidad {modalidad} Quini6 2025', fontsize=16)
    axs[0].grid(axis='y', linestyle='--', alpha=0.8, color='black')
    axs[0].legend(fontsize=16)
    
    # segundo subplot
    orden = np.argsort(cuentas)[::-1]
    valores_ord = valores[orden]
    cuentas_ord = cuentas[orden]
    x_pos = np.arange(len(valores_ord))
    
    axs[1].bar(x_pos, cuentas_ord, color='skyblue', edgecolor='black',
               width=0.6, label=f"Sorteos considerados: {num_sorteos}")
    
    axs[1].set_xticks(x_pos)
    axs[1].set_xticklabels(valores_ord, fontsize=14, rotation=0)
    axs[1].tick_params(axis='y', labelsize=14)
    
    axs[1].set_xlabel('Número', fontsize=14)
    axs[1].set_ylabel('Cantidad de veces sorteado', fontsize=14)
    axs[1].grid(axis='y', linestyle='--', alpha=0.8, color='black')
    axs[1].legend(fontsize=16)
    
    plt.tight_layout()
    plt.show()
#%%

plotear_frecuencias(resultados_tradicional_2025, "tradicional")

plotear_frecuencias(resultados_la_segunda_2025, "la segunda")

plotear_frecuencias(resultados_revancha_2025, "revancha")

plotear_frecuencias(resultados_siempre_sale_2025, "siempre sale")

plotear_frecuencias(resultados_2025, "todos los sorteos")

#%%

"""
test de hipotesis sobre distribucion uniforme para todos los sorteos en 2025, hay 
en el momento de ejecucion del codigo 256 sorteos entre las 4 modalidades.
La hipotesis nula H_0 es que la distribucion de numeros es uniforme, el error de tipo I
lo escojo del 5 %. La distribucion es uniforme discreta, cada numero tiene probabilidad
de 1/46 de salir. uso como estadistico el chi2:
    chi2 = suma de (O_i-E_i)²/E_i²
donde E_i es la frecuencia esperada y O_i la frecuencia observada de cada numero
"""


numeros = resultados_2025[['n1','n2','n3','n4','n5','n6']].values.flatten()

# frecuencias observadas
valores, cuentas = np.unique(numeros, return_counts=True)

# total de observaciones
N = len(numeros)

# frecuencias esperadas bajo H0
esperadas = np.full_like(cuentas, N/46, dtype=float)

# test chi-cuadrado
chi2_stat, p_val = chisquare(cuentas, f_exp=esperadas)

print("Estadístico Chi²:", chi2_stat)
print("p-valor:", p_val)

if p_val < 0.05:
    print("Rechazo H0: la distribucion no es uniforme")
else:
    print("No rechazo H0: no hay evidencia contra la uniformidad")

# calculo de la desviación estandar y media
a, b = 1, 46
n = b - a + 1
var = (n**2 - 1)/12
std = np.sqrt(var)
promedio = (a+b)/2
print(f"La desviación estándar es: {std}")
print(f"El promedio es: {promedio}")

fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(16,7), layout="constrained")

# primer subplot
axs.bar(valores, cuentas, color='skyblue', edgecolor='black',
       width=0.6, label=f"Números sacados: {N} veces")

# lineas horizontales
axs.axhline(promedio, color="black", linestyle="--", label="Media", alpha = 0.7)
axs.axhline(promedio + std, color="red", linestyle="--", label="Media ± 1σ")
axs.axhline(promedio - std, color="red", linestyle="--")

# relleno de color
axs.fill_between(range(-1, 47), promedio - std, promedio + std, color="red", alpha=0.2)

axs.set_xticks(range(0,46))
axs.tick_params(axis='x', labelsize=14, rotation=0)
axs.tick_params(axis='y', labelsize=14)
axs.grid(axis='y', linestyle='--', alpha=0.8, color='black')
axs.set_xlabel('Número', fontsize=16)
axs.set_ylabel('Cantidad de veces sorteado', fontsize=16)
axs.set_title('Distribución de todos los sorteos Quini6 2025', fontsize=16)
axs.grid(axis='y', linestyle='--', alpha=0.8, color='black')
axs.legend(fontsize=14)

plt.show()

#%%



#%%













